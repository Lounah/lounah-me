from typing import Any
from sources.application_state import ApplicationState
from sources.pages.web_page import WebPage
from sources.publications.publication import PublicationType


class PostsPage(WebPage):
    def __init__(self, state: ApplicationState):
        super().__init__("publications.html", state)

    def get_args(self) -> dict[str, Any]:
        return {
            "content": self._get_posts(),
            "type": PublicationType.POST
        }

    def _get_posts(self):
        return list(filter(lambda publication: publication.type == PublicationType.POST, self._state.publications()))


class PodcastsPage(WebPage):
    def __init__(self, state: ApplicationState):
        super().__init__("publications.html", state)

    def get_args(self) -> dict[str, Any]:
        return {
            "content": self._get_podcasts(),
            "type": PublicationType.PODCAST
        }

    def _get_podcasts(self):
        return list(filter(lambda publication: publication.type == PublicationType.PODCAST, self._state.publications()))


class TalksPage(WebPage):
    def __init__(self, state: ApplicationState):
        super().__init__("publications.html", state)

    def get_args(self) -> dict[str, Any]:
        return {
            "content": self._get_talks(),
            "type": PublicationType.TALK
        }

    def _get_talks(self):
        return list(filter(lambda publication: publication.type == PublicationType.TALK, self._state.publications()))
