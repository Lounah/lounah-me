import itertools
from typing import Any

from sources.application_state import ApplicationState
from sources.games.mini_game import MiniGame
from sources.pages.web_page import WebPage


class MainPage(WebPage):
    def __init__(self, state: ApplicationState):
        super().__init__("index.html", state)

    def args(self) -> dict[str, Any]:
        return {
            "all_publications": self._get_posts(),
            "mini_game": MiniGame.random().value
        }

    def _get_posts(self):
        return itertools.groupby(self._state.publications(), lambda publication: publication.type)
