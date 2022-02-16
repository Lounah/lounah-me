from datetime import date
from dataclasses import dataclass
from enum import Enum

import markdown as markdown


class PublicationType(Enum):
    POST = 'Posts'
    PODCAST = 'Podcasts'
    SPEECH = 'Talks'

    def __str__(self):
        return str(self.value)


@dataclass
class PublicationContent:
    text: str

    def overview(self):
        return markdown.markdown(self.text[:450])

    def html(self):
        return markdown.markdown(self.text)


@dataclass
class Publication:
    id: int
    title: str
    date: date
    content: PublicationContent
    type: PublicationType

    def url(self):
        return f"https://lounah.me/blog/{self.id}"
