from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "tournament"
urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("profile/", views.BotPrivateDetailView.as_view(), name="profile"),
    path("profile/edit/", views.BotPrivateUpdateView.as_view(), name="profile_edit"),
    path("bot/<str:name>/", views.BotDetailView.as_view(), name="bot_detail"),
    path("match/<uuid:uuid>/", views.MatchDetailView.as_view(), name="match_detail"),
    path(
        "recent/",
        views.MatchListView.as_view(),
        name="recent_matches",
    ),
    path(
        "visualizer/",
        views.visualizer,
        name="visualizer",
    ),
    path(
        "visualizer/<uuid:match_id>/",
        views.visualizer,
        name="visualizer_match",
    ),
    path(
        "rankings/",
        views.BotListView.as_view(),
        name="bot_list",
    ),
    path(
        "documentation/<str:page_name>/",
        views.documentation,
        name="documentation",
    ),
    path("", TemplateView.as_view(template_name="tournament/index.html"), name="index"),
    path(
        "api/v1/match-result/",
        views.MatchResultView.as_view(),
        name="match_result",
    ),
]
