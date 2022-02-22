import toml

from sources.resources.lang import Lang
from sources.resources.resources_manager import ResourcesManager


class Strings(ResourcesManager):
    def __init__(self, strings_path: str):
        self._strings = toml.load(strings_path)

    def get(self, lang: Lang) -> dict[str, str]:
        strings = self._strings[lang.value]
        strings.update(self._strings['universal'])
        return strings
