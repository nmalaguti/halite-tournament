from django.views import generic

from tournament.models import Match


class MatchDetailView(generic.DetailView):
    model = Match
    paginate_by = 20
    slug_field = "uuid"
    slug_url_kwarg = "uuid"


class MatchListView(generic.ListView):
    model = Match
    paginate_by = 20

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .exclude(date__isnull=True)
            .exclude(replay__isnull=True)
            .exclude(results__isnull=True)
            .order_by("-date")
        )
