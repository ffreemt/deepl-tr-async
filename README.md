# deepl-tr-async ![build](https://github.com/ffreemt/deepl-tr-async/workflows/build/badge.svg)[![codecov](https://codecov.io/gh/ffreemt/deepl-tr-async/branch/master/graph/badge.svg)](https://codecov.io/gh/ffreemt/deepl-tr-async)[![PyPI version](https://badge.fury.io/py/deepl-tr-async.svg)](https://badge.fury.io/py/deepl-tr-async)
deepl translate for free with async and proxy support, based on pyppeteer


### Pre-installation of libicu

###### For Linux/OSX

E.g.
* Ubuntu: `sudo apt install libicu-dev`
* Centos: `yum install libicu`
* OSX: `brew install icu4c`

###### For Windows

Download and install the pyicu and pycld2 whl packages for your OS version from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyicu and https://www.lfd.uci.edu/~gohlke/pythonlibs/#pycld2

### Installation
```pip install deepl-tr-async```

Validate installation
```
python -c "import deepl_tr_async; print(deepl_tr_async.__version__)"
# 0.0.2 or other version info
```

### Usage

#### from the command line 命令行调用
* translate the system clipboad (not tested in Linux) 翻译系统剪贴板
  `deepl-tr`
* translate text supplied from the command line 翻译终端提供的句子
  `deepl-tr --copyfrom=false this is a test`
    <!--img src="img\sample2.png" height="170px" /-->
  ![img](https://raw.githubusercontent.com/ffreemt/deepl-tr-async/master/img/copyfrom-false.png)
* Help 帮助：

  `deepl-tr -?`

  or

  `deepl-tr --helpfull`
    <!--img src="https://github.com/ffreemt/deepl-tr-async/blob/master/img/copyfrom-false.png" height="170px" /-->
  ![img](https://raw.githubusercontent.com/ffreemt/deepl-tr-async/master/img/helpfull.png)

#### Programmatic use 程序调用
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
