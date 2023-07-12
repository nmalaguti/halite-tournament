import gzip
import json
import operator
import os
import tarfile
from datetime import datetime
from functools import reduce

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import models, transaction
from django.db.models import F
from django.db.models.signals import post_save, pre_save

import requests
import trueskill
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from docker_image.reference import InvalidReference, Reference
from dxf import DXF
from dxf.exceptions import DXFUnauthorizedError

from tournament.dataclasses import MatchDataClass


class User(AbstractUser):
    is_npc = models.BooleanField("NPC", default=False)


class BotManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(enabled=True)


class Bot(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    mu = models.FloatField(default=trueskill.MU)
    sigma = models.FloatField(default=trueskill.SIGMA)
    enabled = models.BooleanField(default=True)
    docker_image = models.CharField(max_length=2000, default="", blank=True)
    created_at = CreationDateTimeField()
    updated_at = ModificationDateTimeField()

    objects = BotManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._initial_docker_image = self.docker_image

    def score(self) -> float:
        return self.mu - (self.sigma * 3)

    def rank(self) -> int:
        return (
            Bot.objects.annotate(score=F("mu") - (F("sigma") * 3))
            .filter(score__gt=self.score())
            .count()
            + 1
        )

    def match_count(self):
        return MatchResult.objects.filter(
            bot=self, docker_image=self.docker_image
        ).count()

    def __str__(self):
        return self.name

    @property
    def name(self):
        return self.user.username

    def clean(self):
        if self.docker_image:
            try:
                r = Reference.parse_normalized_named(self.docker_image)
            except InvalidReference as e:
                raise ValidationError({"docker_image": str(e)})

            if r["digest"] is None and r["tag"] is None:
                raise ValidationError(
                    {"docker_image": "a digest or tag must be provided."}
                )

            if r["digest"] is None:

                def auth(dxf_, response):
                    if r.domain() == "ghcr.io":
                        dxf_.authenticate(
                            "USERNAME",
                            settings.GITHUB_READ_PACKAGES_TOKEN,
                            response=response,
                        )
                    if r.domain() == "docker.io":
                        dxf_.authenticate(
                            settings.DOCKER_PUBLIC_READ_USERNAME,
                            settings.DOCKER_PUBLIC_READ_TOKEN,
                            response=response,
                        )

                registry_domain = r.domain()
                if registry_domain == "docker.io":
                    registry_domain = "registry-1.docker.io"

                try:
                    dxf = DXF(registry_domain, r.path(), auth)
                    _, digest = dxf._get_alias(
                        r["tag"],
                        manifest=None,
                        verify=True,
                        sizes=False,
                        get_digest=True,
                        get_dcd=True,
                        get_manifest=False,
                        platform="linux/amd64",
                        ml=True,
                    )
                except DXFUnauthorizedError:
                    raise ValidationError(
                        {
                            "docker_image": "I don't have read access to that registry. Try hosting somewhere else."
                        }
                    )
                except requests.RequestException as e:
                    if e.response is not None:
                        if e.response.status_code == 404:
                            raise ValidationError(
                                {
                                    "docker_image": "Image not found. Check your image and tag."
                                }
                            )
                        elif e.response.status_code == 403:
                            raise ValidationError(
                                {
                                    "docker_image": "I don't have read access to that image. Make sure it is publicly readable."
                                }
                            )

                    raise ValidationError(
                        {
                            "docker_image": "I wasn't able to reach the registry. Check your image."
                        }
                    )

                r = Reference(name=r["name"], tag=r["tag"], digest=digest)

            self.docker_image = r.string()

    @staticmethod
    def create_bot(sender, instance, created, **kwargs):
        if created and not Bot.objects.filter(user=instance).exists():
            Bot.objects.create(user=instance)

    @staticmethod
    def pre_save(sender, instance: "Bot", **kwargs):
        if instance.docker_image != instance._initial_docker_image:
            instance._initial_docker_image = instance.docker_image
            instance.sigma = trueskill.SIGMA


pre_save.connect(Bot.pre_save, sender=Bot, dispatch_uid="bot_pre_save")
post_save.connect(Bot.create_bot, sender=User, dispatch_uid="create_bot")


class Match(models.Model):
    created_at = CreationDateTimeField()
    updated_at = ModificationDateTimeField()

    uuid = models.UUIDField()
    run_id = models.BigIntegerField()

    date = models.DateTimeField(null=True)
    seed = models.PositiveBigIntegerField(null=True)
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    replay = models.FileField(default=None)

    class Meta:
        verbose_name_plural = "matches"

    def __str__(self):
        return str(self.uuid)

    def ordered_results(self):
        return self.results.order_by("rank")

    @staticmethod
    @transaction.atomic
    def create_from_tar(file) -> "Match":
        filename = file.name[:-7]

        with tarfile.open(mode="r", fileobj=file) as result:
            match = MatchDataClass.from_dict(
                json.load(result.extractfile(f"{filename}.json"))
            )

            replay_file = ContentFile(
                gzip.compress(result.extractfile(match.replay).read(), compresslevel=9),
                name=os.path.join(match.id, match.replay + ".gz"),
            )

            match_obj, created = Match.objects.update_or_create(
                uuid=match.id,
                defaults=dict(
                    run_id=match.workflow_run_id,
                    date=datetime.fromisoformat(match.date),
                    seed=match.seed,
                    width=match.width,
                    height=match.height,
                    replay=replay_file,
                ),
            )

            bots = {}

            for match_result in match.match_results:
                bot = Bot.objects.select_for_update().get(
                    user__username=match_result.bot_name
                )
                bots[match_result.bot_name] = bot, match_result

            new_ratings = reduce(
                operator.ior,
                trueskill.rate(
                    [
                        {bot_name: trueskill.Rating(bot.mu, bot.sigma)}
                        for bot_name, (bot, match_result) in bots.items()
                    ],
                    [
                        match_result.rank - 1
                        for bot_name, (bot, match_result) in bots.items()
                    ],
                ),
                {},
            )

            for bot_name, (bot, match_result) in bots.items():
                error_log_file = None
                if match_result.error_log:
                    error_log_file = ContentFile(
                        gzip.compress(
                            result.extractfile(match_result.error_log).read(),
                            compresslevel=9,
                        ),
                        name=os.path.join(match.id, match_result.error_log + ".gz"),
                    )

                rating: trueskill.Rating = new_ratings[bot_name]

                created, match_result_obj = MatchResult.objects.get_or_create(
                    bot=bot,
                    match=match_obj,
                    defaults=dict(
                        docker_image=match_result.docker_image,
                        rank=match_result.rank,
                        mu=rating.mu,
                        sigma=rating.sigma,
                        last_frame_alive=match_result.last_frame_alive,
                        error_log=error_log_file,
                    ),
                )

                if created:
                    bot.mu = rating.mu
                    bot.sigma = rating.sigma
                    bot.save(update_fields=["mu", "sigma", "updated_at"])

        return match_obj


class MatchResult(models.Model):
    bot = models.ForeignKey(Bot, related_name="matches", on_delete=models.CASCADE)
    match = models.ForeignKey(Match, related_name="results", on_delete=models.CASCADE)
    docker_image = models.CharField(max_length=2000)
    rank = models.IntegerField()
    mu = models.FloatField()
    sigma = models.FloatField()
    last_frame_alive = models.IntegerField()
    error_log = models.FileField(default=None)

    created_at = CreationDateTimeField()
    updated_at = ModificationDateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["bot", "match"], name="unique_bot_match")
        ]

    def score(self) -> float:
        return self.mu - (self.sigma * 3)
