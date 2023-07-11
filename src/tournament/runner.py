import json
import random
from collections.abc import Collection
from datetime import datetime, timedelta
from typing import Optional
from uuid import uuid4

from django.conf import settings
from django.db.models import F
from django.db.models.functions import Abs

from github import Auth, Github, Workflow
from github.WorkflowRun import WorkflowRun
from tenacity import RetryError, TryAgain, retry, stop_after_delay, wait_fixed

from tournament.exceptions import (
    TooFewPlayersError,
    TooManyPlayersError,
    WorkflowFailedToStartError,
    WorkflowRunNotFoundError,
)
from tournament.models import Bot, Match

MAP_SIZES = [20, 25, 25, 30, 30, 30, 35, 35, 35, 35, 40, 40, 40, 45, 45, 50]
SEED_NUM_PLAYERS = [2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 6]


@retry(stop=stop_after_delay(60), wait=wait_fixed(3))
def find_run(
    start: datetime, workflow: Workflow, match_id: str
) -> Optional[WorkflowRun]:
    for run in workflow.get_runs(event="workflow_dispatch"):
        if run.created_at < start:
            break

        if run.display_title == match_id:
            return run

    raise TryAgain


def get_players_for_seed(bot: Bot, num_players: Optional[int] = None):
    if num_players is None:
        num_players = random.choice(SEED_NUM_PLAYERS)

    mu_rank_limit = int(5.0 / random.uniform(0.00001, 1) ** 0.65)
    nearby_players = (
        Bot.objects.exclude(pk=bot)
        .exclude(docker_image__exact="")
        .order_by(Abs(F("mu") - bot.mu))[:mu_rank_limit]
    )
    return [bot] + list(
        Bot.objects.filter(pk__in=nearby_players).order_by("?")[: num_players - 1]
    )


def start_match(bots: Collection[Bot]) -> Match:
    if len(bots) < 2:
        raise TooFewPlayersError("Too few players. Minimum 2.")

    if len(bots) > 6:
        raise TooManyPlayersError("Too many players. Maximum 6.")

    auth = Auth.Token(settings.GITHUB_WORKFLOW_TOKEN)
    github = Github(auth=auth)

    workflow = github.get_repo("nmalaguti/halite-matches").get_workflow("match.yml")

    match_id = str(uuid4())
    dimension = random.choice(MAP_SIZES)

    created = workflow.create_dispatch(
        "main",
        {
            "id": match_id,
            "map-size": f"{dimension} {dimension}",
            "bots": json.dumps(
                [
                    {
                        "name": bot.name,
                        "docker-image": bot.docker_image,
                    }
                    for bot in bots
                ]
            ),
        },
    )

    if not created:
        raise WorkflowFailedToStartError("Workflow dispatch did not succeed.")

    try:
        run = find_run(datetime.utcnow() - timedelta(minutes=1), workflow, match_id)
    except RetryError:
        raise WorkflowRunNotFoundError(
            f"Failed to find workflow run with id {match_id}"
        )

    match, created = Match.objects.get_or_create(
        uuid=match_id, defaults=dict(run_id=run.id)
    )

    return match
