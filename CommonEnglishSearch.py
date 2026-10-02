from InflectWrapper import InflectWrapper
import pickle

class CommonEnglishSearch:
    def __init__(self, common_threshold: float = 1.5):
        self._common_threshold = common_threshold
        self._engine = InflectWrapper().inflectEngine

        with open("english_words.pkl", "rb") as f:
            self._freqs = pickle.load(f)

    def GetSingularOrPlural(self, word: str) -> str:
        '''
        Converts the given word to plural if singular and vice versa
        In case of multiple words will convert only the last word
        '''        
        if word is None or word.strip() == '':
            return word
        
        # In case no english alphabet found
        #if re.match('.*[A-Za-z]+.*', word) is None:
        out = word
        if not any(char.isalpha() for char in word):
            out = word
        elif self._engine.singular_noun(word) == False: # not singular
            out = self._engine.plural(word)
        else:
            singular = self._engine.singular_noun(word)
            out = singular if singular != False else word

        return out.strip()

    def IsCommon(self, word: str):
        word = word.lower().strip()
        other_form = self.GetSingularOrPlural(word)
        word_count = 0
        other_count = 0
        if word in self._freqs:
            word_count = self._freqs[word] * 10000

        if other_form in self._freqs:
            other_count = self._freqs[other_form] * 10000

        return max([word_count, other_count]) > self._common_threshold