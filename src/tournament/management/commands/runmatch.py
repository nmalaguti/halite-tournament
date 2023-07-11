import random

from django.core.management.base import BaseCommand, CommandError
from django.db.models import F
from django.db.models.expressions import Func, OuterRef, Subquery
from django.db.models.functions import Abs, Exp, Random
from django.urls import reverse

from tournament.exceptions import HaliteError
from tournament.models import Bot, Match, MatchResult
from tournament.runner import get_players_for_seed, start_match


class Command(BaseCommand):
    help = "Runs a halite match on github."

    def handle(self, *args, **options):
        # https://github.com/HaliteChallenge/Halite/blob/6fe9f685849f26e6e5ea2800b3c3854da23d6a12/website/api/manager/ManagerAPI.php#L79

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

        players = get_players_for_seed(seed_player)

        try:
            match = start_match(players)
        except HaliteError as e:
            raise CommandError(str(e))

        self.stdout.write(
            f"https://halite-tournament.fly.dev"
            + reverse("tournament:match_detail", kwargs=dict(uuid=match.uuid))
        )
