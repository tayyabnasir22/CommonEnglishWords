# common-english-search

Decide whether an English word is "common" — i.e. frequent enough in real usage to be
worth treating as a normal word. Checks the word *and* its singular/plural form, so
`cars`, `Car` and `CARS` all count if `car` is common.

Frequency data comes from the English list in [wordfreq](https://github.com/rspeer/wordfreq)
(~320k words) and is bundled inside the package — no downloads, no setup.

## Installation

From PyPI:

```bash
pip install common-english-search
```

From a local checkout:

```bash
git clone https://github.com/tayyabnasir22/common-english-search.git
cd common-english-search
pip install .
```

For development (editable install + tests):

```bash
pip install -e .
pip install pytest
pytest
```

Requires Python 3.9+. The only runtime dependency is [`inflect`](https://pypi.org/project/inflect/).

## Usage

```python
from common_english_search import CommonEnglishSearch

search = CommonEnglishSearch()

search.IsCommon("house")        # True
search.IsCommon("Houses")       # True  (case-insensitive, plural resolved)
search.IsCommon("xyzzyplonk")   # False

search.AreCommon(["the", "cars", "qwertyuiop"])
# [True, True, False]

search.GetSingularOrPlural("mouse")   # 'mice'
search.GetSingularOrPlural("mice")    # 'mouse'
```

### Threshold

`common_threshold` is the minimum frequency, in **occurrences per 10,000 words**,
for a word to count as common. The default is `1.5`.

```python
strict = CommonEnglishSearch(common_threshold=5.0)   # fewer words count as common
loose  = CommonEnglishSearch(common_threshold=0.1)   # more words count as common
```

## License

Code: Apache-2.0. Data: CC BY-SA 4.0, derived from wordfreq by Robyn Speer — see `LICENSE`.