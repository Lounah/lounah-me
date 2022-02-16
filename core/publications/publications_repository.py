import itertools

from core.publications.publication import PublicationType
from core.publications.publications_source import PublicationsSource


class PublicationsRepository:

    def __init__(self, source: PublicationsSource):
        self._source = source

    def get_all_grouped(self):
        return itertools.groupby(self._source.resolve(), lambda publication: publication.type)

    def get_all_by_type(self, publication_type: PublicationType):
        return list(filter(lambda publication: publication.type == publication_type, self._source.resolve()))

    def get_by_id(self, id):
        return next(filter(lambda post: post.id == id, self._source.resolve()))
