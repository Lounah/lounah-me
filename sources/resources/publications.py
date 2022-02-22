from sources.publications.publication import Publication
from sources.publications.publications_source import PublicationsSource
from sources.resources.lang import Lang
from sources.resources.resources_manager import ResourcesManager


class Publications(ResourcesManager):
    def __init__(self, sources: dict[Lang, PublicationsSource]):
        self._sources = sources

    def get(self, lang: Lang) -> list[Publication]:
        return self._sources[lang].resolve()
