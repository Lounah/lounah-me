from sources.publications.publication import Publication
from sources.resources.lang import Lang
from sources.resources.publications import Publications
from sources.resources.strings import Strings


class ApplicationState:
    def __init__(self, strings: Strings, publications: Publications, default_lang: Lang):
        self.lang = default_lang
        self._strings = strings
        self._publications = publications

    def strings(self) -> dict[str, str]:
        return self._strings.get(self.lang)

    def publications(self) -> list[Publication]:
        return self._publications.get(self.lang)
