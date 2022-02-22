from typing import Any
from sources.application_state import ApplicationState
from sources.pages.web_page import WebPage


class PublicationPage(WebPage):
    def __init__(self, id: str, state: ApplicationState):
        super().__init__("publication.html", state)
        self.id = id

    def get_args(self) -> dict[str, Any]:
        return {"publication": self._get_publication_by_id()}

    def _get_publication_by_id(self):
        return list(filter(lambda publication: publication.id == self.id, self._state.publications()))[0]
