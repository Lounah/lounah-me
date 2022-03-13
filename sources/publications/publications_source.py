import abc
import datetime
import os
from pathlib import Path

from sources.publications.publication import Publication, PublicationType, PublicationContent


class PublicationsSource:

    @abc.abstractmethod
    def resolve(self) -> list[Publication]:
        """
        Represents a source of publication:
        TODO
        :return:
        """
        pass


class StaticPublicationSource(PublicationsSource):

    def __init__(self, static_source_path: str):
        self._path = static_source_path

    def resolve(self) -> list[Publication]:
        all_publications = self._extract_contents()
        return list(map(self._md_to_publication, all_publications))

    def _extract_contents(self) -> list[str]:
        result = []
        for root, directories, files in os.walk(self._path):
            for name in files:
                result.append(os.path.join(root, name))
        return result

    @staticmethod
    def _md_to_publication(publication_md) -> Publication:
        path = Path(publication_md)
        content = PublicationContent(path.read_text(encoding='utf-8', errors='ignore'))
        return Publication(
            id=path.stem,
            title=content.title(),
            content=content,
            type=PublicationType(path.parent.name.capitalize()),
            date=datetime.datetime.fromtimestamp(os.path.getctime(publication_md))
        )
