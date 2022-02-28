from enum import Enum


class Lang(Enum):
    RU = 'ru'
    EN = 'en'

    @staticmethod
    def values():
        return ['ru', 'en']

    @staticmethod
    def best_match(languages: list[str]):
        if Lang.RU.value in languages:
            return Lang.RU
        elif Lang.EN.value in languages:
            return Lang.EN
        else:
            return Lang.RU
