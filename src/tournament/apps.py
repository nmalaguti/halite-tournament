import logging
from functools import cache

from django.apps import AppConfig
from django.db import OperationalError
from django.db.backends.base.base import BaseDatabaseWrapper

import trueskill
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

# https://janzert.com/halite/rating-report/
# https://web.archive.org/web/20210126111322/http://2016.forums.halite.io/t/the-unofficial-better-final-rankings/1000.html
# https://github.com/Janzert/halite_ranking/tree/master
trueskill.setup(tau=0.0, draw_probability=0.0, backend="mpmath")

# TODO: explore global rankings with choix updated regularly

logger = logging.getLogger(__name__)


@cache
def monkey_patch():
    BaseDatabaseWrapper.ensure_connection = retry(
        retry=retry_if_exception_type(OperationalError),
        stop=stop_after_attempt(6),
        wait=wait_exponential(min=1, max=10),
        before_sleep=before_sleep_log(logger, logging.INFO),
        reraise=True,
    )(BaseDatabaseWrapper.ensure_connection)


class TournamentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tournament"

    def ready(self):
        monkey_patch()
