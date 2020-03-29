# deepl-tr-async ![build](https://github.com/ffreemt/deepl-tr-async/workflows/build/badge.svg)[![codecov](https://codecov.io/gh/ffreemt/deepl-tr-async/branch/master/graph/badge.svg)](https://codecov.io/gh/ffreemt/deepl-tr-async)[![PyPI version](https://badge.fury.io/py/deepl-tr-async.svg)](https://badge.fury.io/py/deepl-tr-async)
deepl translate for free with async and proxy support, based on pyppeteer

### Installation

```pip install deepl-tr-async```

Validate installation
```
python -c "import deepl_tr_async; print(deepl_tr_async.__version__)"
# 0.0.1 or other version info
```

### Usage

```
import asyncio
from deepl_tr_async import deepl_tr_async
from deepl_tr_async.google_tr_async import google_tr_async

loop = asyncio.get_event_loop()

sent = 'Global coronavirus pandemic kills more than 30,000'

res = loop.run_until_complete(deepl_tr_async(sent, to_lang='zh'))
print(res)
# Alternatives:
# 全球冠状病毒大流行导致超过3万人死亡
# 全球冠状病毒大流行导致3万多人死亡
# 全球冠状病毒大流行导致超过30,000人死亡
# 全球冠状病毒大流行导致3万多人丧生

res = loop.run_until_complete(google_tr_async(sent, to_lang='zh'))
print(res)
# 全球冠状病毒大流行杀死超过30,000人

tasks = [deepl_tr_async(sent, to_lang='zh'), google_tr_async(sent, to_lang='zh')]
_ = asyncio.gather(*tasks)
res = loop.run_until_complete(_)
print(res)
['Alternatives:\n全球冠状病毒大流行导致超过3万人死亡\n全球冠状病毒大流行导致3万多人死亡\n全球冠状病毒大流行导致超过30,000人死亡\n全球冠状病毒大流行导致3万多人丧生', '全球冠状病毒大流行杀死超过30,000人']
```

## Extra installation for Windows 10

Download and install the pyicu and pycld2 whl packages for your OS version from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyicu and https://www.lfd.uci.edu/~gohlke/pythonlibs/#pycld2
