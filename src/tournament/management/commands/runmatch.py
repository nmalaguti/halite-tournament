import json
import random
from datetime import datetime, timedelta
from time import sleep
from typing import Optional
from uuid import uuid4

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models import F
from django.db.models.expressions import Func, OuterRef, Subquery
from django.db.models.functions import Abs, Exp, Random
from django.urls import reverse

from github import Auth, Github
from github.WorkflowRun import WorkflowRun

from tournament.models import Bot, Match, MatchResult

MAP_SIZES = [20, 25, 25, 30, 30, 30, 35, 35, 35, 35, 40, 40, 40, 45, 45, 50]
SEED_NUM_PLAYERS = [2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 6]


class Command(BaseCommand):
    help = "Runs a halite match on github."

    def handle(self, *args, **options):
        self.start = datetime.utcnow() - timedelta(minutes=1)

        auth = Auth.Token(settings.GITHUB_WORKFLOW_TOKEN)
        github = Github(auth=auth)

        self.workflow = github.get_repo("nmalaguti/halite-matches").get_workflow(
            "match.yml"
        )

        dimension = random.choice(MAP_SIZES)
        self.match_id = str(uuid4())

        self.stdout.write(
            f"Match ID: {self.match_id}, Dimensions: {dimension} {dimension}, "
        )

        # https://github.com/HaliteChallenge/Halite/blob/6fe9f685849f26e6e5ea2800b3c3854da23d6a12/website/api/manager/ManagerAPI.php#L79
        # pick num players
        num_players = random.choice(SEED_NUM_PLAYERS)

        # pick seed player
        # 50%: pick a player at random weighted by their sigma (uncertainty)
        # 25%: pick a player with less than N games from the top 15 players who played a game the longest ago
        seed_selection = random.choice([1, 1, 2, 3])
        if seed_selection == 1:
            # 25%: pick the player who hasn't played a game in the longest amount of time
            seed_player = (
                Bot.objects.exclude(docker_image__exact="")
                .exclude(user__is_npc=True)
                .order_by((Random() * Exp("sigma")).desc())
                .first()
            )
        elif seed_selection == 2:
            # 25%: pick a player with less than 400 games from the top 15 players who played a game the longest ago
            seed_player = random.choice(
                Bot.objects.exclude(docker_image__exact="")
                .exclude(user__is_npc=True)
                .annotate(
                    last_game_date=Subquery(
                        Match.objects.filter(
                            results__bot=OuterRef("pk"),
                            results__bot__docker_image=OuterRef("docker_image"),
                        )
                        .order_by("-date")
                        .values("date")[:1]
                    ),
                    match_count=Subquery(
                        MatchResult.objects.filter(
                            bot=OuterRef("pk"), docker_image=OuterRef("docker_image")
                        )
                        .annotate(count=Func(F("pk"), function="Count"))
                        .values("count")
                    ),
                )
                .filter(match_count__lt=400)
                .order_by("last_game_date")[:15]
            )
        else:  # seed_selection == 3
            # 25%: pick the player who hasn't played a game in the longest amount of time
            seed_player = (
                Bot.objects.exclude(docker_image__exact="")
                .exclude(user__is_npc=True)
                .annotate(
                    last_game_date=Subquery(
                        Match.objects.filter(
                            results__bot=OuterRef("pk"),
                            results__bot__docker_image=OuterRef("docker_image"),
                        )
                        .order_by("-date")
                        .values("date")[:1]
                    ),
                )
                .order_by("last_game_date")
                .first()
            )

        mu_rank_limit = int(5.0 / random.uniform(0.00001, 1) ** 0.65)
        nearby_players = (
            Bot.objects.exclude(pk=seed_player)
            .exclude(docker_image__exact="")
            .order_by(Abs(F("mu") - seed_player.mu))[:mu_rank_limit]
        )
        players = [seed_player] + list(
            Bot.objects.filter(pk__in=nearby_players).order_by("?")[:num_players]
        )

        created = self.workflow.create_dispatch(
            "main",
            {
                "id": self.match_id,
                "map-size": f"{dimension} {dimension}",
                "bots": json.dumps(
                    [
                        {
                            "name": player.user.username,
                            "docker-image": player.docker_image,
                        }
                        for player in players
                    ]
                ),
            },
        )

        if not created:
            raise CommandError("Failed to start workflow")

        run = self.find_run()
        if run is None:
            raise CommandError(f"Couldn't find run matching {self.match_id}")

        match, created = Match.objects.get_or_create(
            uuid=self.match_id, defaults=dict(run_id=run.id)
        )

        self.stdout.write(
            f"https://halite-tournament.fly.dev"
            + reverse("tournament:match_detail", kwargs=dict(uuid=match.uuid))
        )

    def find_run(self) -> Optional[WorkflowRun]:
        retries = 20
        for i in range(retries):
            for run in self.workflow.get_runs(event="workflow_dispatch"):
                if run.created_at < self.start:
                    break

                if run.display_title == self.match_id:
                    return run
            if i < retries - 1:
                sleep(3)
        return None
