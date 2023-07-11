from django import forms
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UsernameField
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from .exceptions import HaliteError
from .models import Bot, Match, MatchResult, User
from .runner import get_players_for_seed, start_match


class BotAdmin(admin.ModelAdmin):
    list_display = ["__str__", "docker_image", "enabled"]

    actions = ["run_match", "run_match_with_seed_player"]

    @admin.action(description="Run match with selected bots")
    def run_match(self, request, queryset):
        try:
            match = start_match(queryset)
        except HaliteError as e:
            self.message_user(
                request, f"Failed to start match: {e}", level=messages.ERROR
            )
            return

        self.message_user(
            request,
            mark_safe(
                f"""Match started <a href="https://github.com/nmalaguti/halite-matches/actions/runs/{match.run_id}">{match.uuid}</a>"""
            ),
            level=messages.SUCCESS,
        )

    @admin.action(description="Run match with bot as seed player")
    def run_match_with_seed_player(self, request, queryset):
        if len(queryset) > 1:
            self.message_user(
                request, "Pick a single bot to be the seed player", level=messages.ERROR
            )
            return

        bots = get_players_for_seed(queryset[0])
        try:
            match = start_match(bots)
        except HaliteError as e:
            self.message_user(
                request, f"Failed to start match: {e}", level=messages.ERROR
            )
            return

        self.message_user(
            request,
            mark_safe(
                f"""Match started <a href="https://github.com/nmalaguti/halite-matches/actions/runs/{match.run_id}">{match.uuid}</a>"""
            ),
            level=messages.SUCCESS,
        )

    def has_delete_permission(self, request, obj=None):
        return False


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username
    """

    class Meta:
        model = User
        fields = ("username", "is_npc")
        field_classes = {"username": UsernameField, "is_npc": forms.BooleanField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs[
                "autofocus"
            ] = True

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_unusable_password()
        if commit:
            user.save()
            if hasattr(self, "save_m2m"):
                self.save_m2m()
        return user

    def clean_username(self):
        """Reject usernames that differ only in case."""
        username = self.cleaned_data.get("username")
        if (
            username
            and self._meta.model.objects.filter(username__iexact=username).exists()
        ):
            self._update_errors(
                ValidationError(
                    {
                        "username": self.instance.unique_error_message(
                            self._meta.model, ["username"]
                        )
                    }
                )
            )
        else:
            return username


class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "is_npc"),
            },
        ),
    )
    fieldsets = (
        (None, {"fields": ("username", "is_npc")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_npc",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "groups", "is_npc")


class MatchUploadForm(forms.ModelForm):
    match_file = forms.FileField()

    def clean(self):
        super().clean()

        if not self.cleaned_data["match_file"].name.endswith(".tar.xz"):
            self.add_error("match_file", "Match file must be a .tar.xz file")
        else:
            try:
                self.instance = Match.create_from_tar(self.cleaned_data["match_file"])
            except Exception as e:
                self.add_error("match_file", e)

    class Meta:
        model = Match
        fields = []


class MatchAdmin(admin.ModelAdmin):
    add_form = MatchUploadForm
    list_display = ["uuid", "run_id", "date", "seed", "width", "height", "participants"]

    @admin.display(description="Participants")
    def participants(self, obj):
        return ", ".join([result.bot.name for result in obj.results.all()])

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        defaults = {}
        if obj is None:
            defaults["form"] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)


class MatchResultAdmin(admin.ModelAdmin):
    list_display = ["match", "bot", "rank"]

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(User, UserAdmin)
admin.site.register(Bot, BotAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(MatchResult, MatchResultAdmin)
