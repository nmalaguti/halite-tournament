from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import F, Func, OuterRef, Subquery, Window
from django.db.models.functions import Rank
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic

from crispy_forms.layout import Submit

from tournament.models import Bot, MatchResult

from .generic import DetailListView, FormHelperMixin


class BotListView(generic.ListView):
    model = Bot
    paginate_by = 20

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(enabled=True)
            .annotate(
                rank=Window(
                    expression=Rank(), order_by=(F("mu") - (F("sigma") * 3)).desc()
                ),
                match_count=Subquery(
                    MatchResult.objects.filter(
                        bot=OuterRef("pk"), docker_image=OuterRef("docker_image")
                    )
                    .annotate(count=Func(F("pk"), function="Count"))
                    .values("count")
                ),
            )
            .order_by((F("mu") - (F("sigma") * 3)).desc(), "-mu", "user__username")
        )


class BotPrivateDetailView(LoginRequiredMixin, DetailListView):
    model = Bot
    paginate_by = 20
    template_name_suffix = "_private_detail"

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, user=self.request.user)

    def get_object_list(self):
        return (
            MatchResult.objects.filter(bot=self.get_object())
            .exclude(match__replay__isnull=True)
            .order_by("-match__date")
        )


class BotPrivateUpdateView(
    LoginRequiredMixin, SuccessMessageMixin, FormHelperMixin, generic.UpdateView
):
    model = Bot
    fields = ["docker_image"]
    template_name_suffix = "_private_update"
    success_message = "Updated Docker Image successfully!"

    def get_helper(self):
        helper = super().get_helper()

        helper.form_method = "post"
        helper.add_input(Submit("submit", "Submit"))

        return helper

    def get_success_url(self):
        return reverse("tournament:profile")

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, user=self.request.user)


class BotDetailView(DetailListView):
    model = Bot
    paginate_by = 20
    slug_field = "user__username"
    slug_url_kwarg = "name"

    def get_object_list(self):
        return (
            MatchResult.objects.filter(bot=self.get_object())
            .exclude(match__replay__isnull=True)
            .order_by("-match__date")
        )
