import pickle
from importlib import resources
from .inflect_wrapper import InflectWrapper

def _load_freqs() -> dict[str, float]:
    '''Load the bundled English frequency dict shipped inside the package.'''
    data_file = resources.files(__package__).joinpath("data", "english_words.pkl")
    with data_file.open("rb") as f:
        return pickle.load(f)


class CommonEnglishSearch:
    def __init__(self, common_threshold: float = 1.5):
        self._common_threshold = common_threshold
        self._freq_threshold = common_threshold / 10000
        self._engine = InflectWrapper().inflectEngine
        self._inflect_cache: dict[str, str] = {}
        self._freqs = _load_freqs()

    def GetSingularOrPlural(self, word: str) -> str:
        '''
        Converts the given word to plural if singular and vice versa
        In case of multiple words will convert only the last word
        '''
        if word is None or word.strip() == '':
            return word

        cached = self._inflect_cache.get(word)
        if cached is not None:
            return cached

        if not any(char.isalpha() for char in word):
            out = word
        else:
            singular = self._engine.singular_noun(word)
            if singular is False:
                out = self._engine.plural(word)
            else:
                out = singular

        out = out.strip()
        self._inflect_cache[word] = out
        return out

    def _is_common_normalized(self, word: str) -> bool:
        if self._freqs.get(word, 0.0) > self._freq_threshold:
            return True
        return self._freqs.get(self.GetSingularOrPlural(word), 0.0) > self._freq_threshold

    def IsCommon(self, word: str) -> bool:
        return self._is_common_normalized(word.lower().strip())

    def AreCommon(self, words: list[str]) -> list[bool]:
        return [self._is_common_normalized(w.lower().strip()) for w in words]
