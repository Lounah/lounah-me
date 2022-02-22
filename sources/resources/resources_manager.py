import abc

from sources.resources.lang import Lang


class ResourcesManager:

    @abc.abstractmethod
    def get(self, lang: Lang):
        pass
