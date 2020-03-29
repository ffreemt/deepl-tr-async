# deepl-tr-async ![build](https://github.com/ffreemt/deepl-tr-async/workflows/build/badge.svg)[![codecov](https://codecov.io/gh/ffreemt/deepl-tr-async/branch/master/graph/badge.svg)](https://codecov.io/gh/ffreemt/deepl-tr-async)
deepl translate for free with async and proxy support, based on pyppeteer

### Installation
Not available yet
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

asyncio.get_event_loop().run_until_complete(deep_tr_async('test this and that'))
# '测试这个和那个'
```

## Extra installation for Windows 10

Download and install the pyicu and pycld2 whl packages for your OS version from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyicu and https://www.lfd.uci.edu/~gohlke/pythonlibs/#pycld2

### Acknowledgments

* Thanks to everyone whose code was used
