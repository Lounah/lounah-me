import datetime
import itertools

from core.publications.publication import Publication, PublicationContent, PublicationType


class PublicationsStore:

    _internal_storage = [
        Publication(
            id=0,
            title="Отключаем Jetifier и ускоряем сборку",
            date=datetime.date(2020, 12, 30),
            content=PublicationContent(open("jetifier.md").read()),
            type=PublicationType.POST
        ),
        Publication(
            id=1,
            title="Как Java 8 поддерживается в Android",
            date=datetime.date(2019, 12, 4),
            content=PublicationContent("Blah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blah"),
            type=PublicationType.POST
        ),
        Publication(
            id=0,
            title="TeamCity: настраиваем CI/CD в вашей команде",
            date=datetime.date(2020, 12, 14),
            content=PublicationContent("Blah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blahBlah-blah-blah-blah"),
            type=PublicationType.POST
        ),
        Publication(
            id=0,
            title="TeamCity: настраиваем CI/CD в вашей команде",
            date=datetime.date(2020, 12, 14),
            content=PublicationContent("Blah-blah-blah-blah"),
            type=PublicationType.PODCAST
        ),
        Publication(
            id=0,
            title="TeamCity: настраиваем CI/CD в вашей команде",
            date=datetime.date(2020, 12, 14),
            content=PublicationContent("Blah-blah-blah-blah"),
            type=PublicationType.PODCAST
        ),
        Publication(
            id=0,
            title="TeamCity: настраиваем CI/CD в вашей команде",
            date=datetime.date(2020, 12, 14),
            content=PublicationContent("Blah-blah-blah-blah"),
            type=PublicationType.PODCAST
        ),
        Publication(
            id=0,
            title="TeamCity: настраиваем CI/CD в вашей команде",
            date=datetime.date(2020, 12, 14),
            content=PublicationContent("Blah-blah-blah-blah"),
            type=PublicationType.SPEECH
        ),
        Publication(
            id=0,
            title="TeamCity: настраиваем CI/CD в вашей команде",
            date=datetime.date(2020, 12, 14),
            content=PublicationContent("Blah-blah-blah-blah"),
            type=PublicationType.SPEECH
        ),
        Publication(
            id=0,
            title="TeamCity: настраиваем CI/CD в вашей команде",
            date=datetime.date(2020, 12, 14),
            content=PublicationContent("Blah-blah-blah-blah"),
            type=PublicationType.SPEECH
        )
    ]

    def get_all_grouped(self):
        return itertools.groupby(self._internal_storage, lambda publication: publication.type)

    def get_posts(self):
        return list(filter(lambda publication: publication.type == PublicationType.POST, self._internal_storage))
