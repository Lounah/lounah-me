from typing import Any
from sources.application_state import ApplicationState
from sources.pages.web_page import WebPage


class ResumePage(WebPage):
    def __init__(self, state: ApplicationState):
        super().__init__("resume.html", state)

    def args(self) -> dict[str, Any]:
        return {"publication": self._state.resume()}
