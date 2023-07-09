from django.contrib import messages
from django.contrib.auth import logout as logout_user
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect
from django.urls import reverse


def login(request):
    return redirect_to_login(
        request.GET.get("next", ""),
        reverse("social:begin", kwargs=dict(backend="github")),
    )


def logout(request):
    logout_user(request)
    messages.success(request, "Logged out!")
    return redirect("tournament:index")
