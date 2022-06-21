import abc
from typing import Any

from flask import render_template, request

from sources.application_state import ApplicationState
from sources.resources.lang import Lang


class WebPage:
    def __init__(self, html: str, state: ApplicationState):
        self.html = html
        self._state = state

    @abc.abstractmethod
    def args(self) -> dict[str, Any]:
        pass

    def create(self):
        self._state.lang = self._get_language()
        return render_template(self.html, strings=self._state.strings(), **self.args())

    @staticmethod
    def _get_language() -> Lang:
        """
        Temporally use 'ru' lang as project's default.
        Will be fixed as soon as I will write more english-based content.
        """
        return Lang.best_match(request.cookies.get('lang', default=['ru']))
