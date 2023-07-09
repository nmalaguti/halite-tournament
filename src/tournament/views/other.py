from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.template import TemplateDoesNotExist

from tournament.models import Match


def visualizer(request, match_id=None):
    replay_url = None
    if match_id is not None:
        match = get_object_or_404(Match, uuid=match_id)
        replay_url = match.replay.url
    return render(
        request, "tournament/visualizer.html", context=dict(replay_url=replay_url)
    )


def documentation(request, page_name: str):
    try:
        return render(
            request,
            f"tournament/documentation/{page_name}.html",
            context={"page_name": page_name},
        )
    except TemplateDoesNotExist:
        raise Http404("Page does not exist.")
