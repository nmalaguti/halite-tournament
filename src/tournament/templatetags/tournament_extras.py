import os
from datetime import datetime
from typing import Optional

from django import template
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.utils.safestring import mark_safe

from tournament.models import Bot

register = template.Library()


@register.filter
def bootstrap_alert(value):
    if value == "error":
        return "alert-danger"

    if value == "debug":
        return "alert-info"

    return f"alert-{value}"


@register.filter
def localized_datetime(date_time: datetime):
    return mark_safe(
        f"""<span data-date-time="{date_time.isoformat()}">{date_time.strftime("%m/%d/%Y %I:%M:%S %p %Z")}</span>"""
    )


@register.simple_tag
def minimal_replay(replay_file: str, height=500):
    replay_file_url = static(os.path.join("tournament/replays", replay_file))
    return mark_safe(
        f"""<div class="thumbnail center-block replay" data-replay-url="{replay_file_url}" data-replay-is-minimal="true" data-replay-max-height="{height}"></div>"""
    )


@register.simple_tag
def replay(replay_file: str, height=500):
    replay_file_url = static(os.path.join("tournament/replays", replay_file))
    return mark_safe(
        f"""<div class="thumbnail center-block replay" data-replay-url="{replay_file_url}" data-replay-max-height="{height}"></div>"""
    )


BOT_ICONS = {
    "easybot": {
        "path": "bot.png",
        "attribution": """<a href="https://www.flaticon.com/free-icons/robot" title="robot icons">Robot icons created by Smashicons - Flaticon</a>""",
    },
    "novicebot": {
        "path": "robot.png",
        "attribution": """<a href="https://www.flaticon.com/free-icons/robot" title="robot icons">Robot icons created by Freepik - Flaticon</a>""",
    },
    "erdman_v12": {
        "path": "robot_2.png",
        "attribution": """<a href="https://www.flaticon.com/free-icons/futurist" title="futurist icons">Futurist icons created by Freepik - Flaticon</a>""",
    },
    "bot_2": {
        "path": "bot_2.png",
        "attribution": """<a href="https://www.flaticon.com/free-icons/robot" title="robot icons">Robot icons created by Flowicon - Flaticon</a>""",
    },
    "notgreat": {
        "path": "chatbot.png",
        "attribution": """<a href="https://www.flaticon.com/free-icons/question-mark" title="question mark icons">Question mark icons created by Freepik - Flaticon</a>""",
    },
}


@register.filter
def bot_profile_pic(bot: Bot):
    bot_pic = BOT_ICONS.get(
        bot.name,
        {
            "path": "robot-assistant.png",
            "attribution": """<a href="https://www.flaticon.com/free-icons/botnet" title="botnet icons">Botnet icons created by juicy_fish - Flaticon</a>""",
        },
    )
    img_src = static(os.path.join("tournament/icons", bot_pic["path"]))
    attribution = bot_pic["attribution"]

    return mark_safe(
        f"""
        <img src="{img_src}" class="img-responsive center-block img-thumbnail" style="background-color: #f8fafb; border-radius: 5%; background-clip: content-box;" width="252px" height="252px">
        <p style="font-size: x-small; padding-top: 8px" class="text-center">{attribution}</p>
        """
    )


@register.filter
def bot_icon_url(bot: Bot):
    bot_pic = BOT_ICONS.get(
        bot.name,
        {
            "path": "robot-assistant.png",
            "attribution": """<a href="https://www.flaticon.com/free-icons/botnet" title="botnet icons">Botnet icons created by juicy_fish - Flaticon</a>""",
        },
    )
    return static(os.path.join("tournament/icons", bot_pic["path"]))


@register.simple_tag
def bot_link(bot: Bot, self: Optional[Bot] = None):
    return mark_safe(
        render_to_string(
            "tournament/tag_partials/bot_link.html", dict(bot=bot, self=self)
        ).strip()
    )
