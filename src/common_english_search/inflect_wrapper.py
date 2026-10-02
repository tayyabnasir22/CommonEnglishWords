import inflect

from .singleton import Singleton


class InflectWrapper(Singleton):
    def __init__(self) -> None:
        self._inflectEngine = inflect.engine()

    @property
    def inflectEngine(self):
        '''inflect.engine()'''
        return self._inflectEngine
