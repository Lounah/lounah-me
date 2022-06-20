import re
from datetime import date
from dataclasses import dataclass
from enum import Enum

import markdown as markdown


class PublicationType(Enum):
    POST = 'Posts'
    PODCAST = 'Podcasts'
    TALK = 'Talks'

    def translated(self, strings: dict[str, str]) -> str:
        return strings[self.value.lower()]

    def order(self):
        if self == PublicationType.POST:
            return 0
        elif self == PublicationType.TALK:
            return 1
        elif self == PublicationType.PODCAST:
            return 2

    def __str__(self):
        return str(self.value)


class PublicationContent:
    def __init__(self, text):
        self.text = text
        self.html = markdown.markdown(text)

    def overview(self):
        content = self.text.split('[overview]: <>')[0]
        return markdown.markdown(content)

    def title(self):
        """
        Extract publication title from the very first <h1> tag;
        Also remove '#' characters.
        :return: publication title
        """
        pattern = "<h1>(.*?)</h1>"
        title = re.search(pattern, self.html).group(1)
        return title.replace("#", "")


@dataclass
class Publication:
    id: str
    title: str
    date: date
    content: PublicationContent
    type: PublicationType

    def url(self):
        return f"/publications/{self.id}"
