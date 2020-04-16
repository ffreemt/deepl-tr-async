"""
deepl via pyppeteer

proxy = '103.28.206.65:888'
browser = await launch(
    headless=False,
    args=['--proxy-server={}'.format(proxy), ]
)

await page.goto('http://www.chenxm.cc/', {'timeout': 10000*20})

pip3.6 uninstall websockets  # 卸载websockets
pip3.6 install websockets==6.0  # 指定安装6.0版本```

https://hacpai.com/article/1566221786951
    '--window-size=1440x900'
    autoClose（bool）：脚本完成时自动关闭浏览器进程。默认为 True
https://zhuanlan.zhihu.com/p/97424787
    ["--disable-infobars",
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",]

await page.setViewport({'width': 1366, 'height': 768})

https://github.com/miyakogi/pyppeteer/pull/160/files
pyppeteer/connection.py line:44 -+
            self._url, max_size=None, loop=self._loop)
            self._url, max_size=None, loop=self._loop, ping_interval=None, ping_timeout=None)
pip install websockets==6.0 -U
poetry add websockets==6.0

# https://www.jianshu.com/p/611ed6b75d47
await page.setViewport(viewport={'width':1280, 'height':800})
await page.setJavaScriptEnabled(enabled=True)
await page.xpath('//div[@class="title-box"]/a')

while not await page.querySelector('.t'):
    pass
await page.screenshot({'path': 'example.png'})

$变为querySelector
# Pyppeteer使用Python风格的函数名
Page.querySelector()/Page.querySelectorAll()/Page.xpath()
# 简写方式为：
Page.J(), Page.JJ(), and Page.Jx()

googlecn:
de-zh zh-CN
f"https://translate.google.cn/#view=home&op=translate&sl=de&tl=de&text={text}"

en-zh zh-CN
https://translate.google.cn/#view=home&op=translate&sl=zh-CN&tl=de&text={text}"

.result-shield-container
pq(content)(".result-shield-container").text()

async fetch(url, css, browser=None):

sys pyppeteer  0.0.17 websockets
poetry pyppeteer 0.0.25 websockets 6.0
"""
# pylint: disable=too-many-arguments, too-many-locals
# pylint: disable=too-many-statements, too-many-branches
# pylint: disable=unused-import

from typing import Any, List, Optional, Tuple, Union

# import os
# from pathlib import Path
import asyncio
from timeit import default_timer
from urllib.parse import quote

# from textwrap import wrap
# from pyperclip import copy

from pyppeteer import launch
from pyquery import PyQuery as pq

# import langid
from polyglot.detect import Detector
import logzero
from logzero import logger
# import dotenv
# from environs import Env

from deepl_tr_async.load_env import load_env

# preload to memory
# langid.classify("")

# browser = await launch(headless=False)

URL = r"https://www.deepl.com/translator"
LOOP = asyncio.get_event_loop()

# dotenv.load_dotenv(verbose=1)
# in shell or in .env
# set HEADFUL=anything (include 0 False) to show browser

_ = """
ENV = Env()
logger.info(" dotenv.find_dotenv(Path().cwd() / \".env\"): %s", Path().cwd() / '.env')
_ = dotenv.find_dotenv(Path().cwd() / ".env")
if _:
    logger.info(" Loading .env [%s]...", _)
    ENV.read_env(_, override=1)

try:
    HEADFUL = ENV.bool("HEADFUL")
except Exception as exc:
    logger.warning(' env.bool("HEADFUL") exc: %s', exc)
    HEADFUL = False
try:
    DEBUG = ENV.bool("DEBUG")
except Exception as exc:
    logger.warning(
        ' env.bool("DEBUG") [%s] exc: %s, DEBUG setting to False',
        os.getenv("DEBUG"),
        exc,
    )
    DEBUG = False
try:
    PROXY = ENV.str("PROXY")
except Exception as exc:
    logger.warning(' env.str("PROXY") exc: %s', exc)
    PROXY = ""
# """

try:
    HEADFUL = bool(load_env("headful", "bool"))
except Exception as exc:
    logger.info("exc: %s", exc)
    HEADFUL = False
try:
    DEBUG = bool(load_env("DEBUG", "bool"))
except Exception as exc:
    logger.info("exc: %s", exc)
    DEBUG = False
try:
    PROXY = str(load_env("PROXY", "str"))
except Exception as exc:
    logger.info("exc: %s", exc)
    PROXY = ""

logger.info(" HEADFUL: %s", HEADFUL)
logger.info(" DEBUG: %s", DEBUG)
logger.info(" PROXY: %s", PROXY)


async def get_ppbrowser(headless=not HEADFUL, proxy: str = PROXY):
    """ get a puppeeter browser"""
    try:
        browser = await launch(
            args=[
                "--disable-infobars",
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
                "--window-size=1440x900",
                # "--autoClose=False",
                # f"--proxy-server={PROXY}",
                f"--proxy-server={proxy}",
            ],
            # autoClose=False,
            headless=headless,
            dumpio=True,
            userDataDir="",
        )
    except Exception as exc:
        logger.error("get_ppbrowser exc: %s", exc)
        raise
    # page = await browser.newPage()
    # await page.goto(url)
    # logger.debug("page.goto deepl time: %.2f s", default_timer() - then)
    return browser


try:
    BROWSER = LOOP.run_until_complete(get_ppbrowser(not HEADFUL))
except Exception as exc:
    logger.error(" Unable to pyppeteer.launch exc: %s", exc)
    logger.info(
        "\n\t%s",
        r"Possible cause: abnormal exit from a previous session. Try `taskkill /f /im chrome.exe`",
    )
    logger.warning(" %s", "Note that this will also kill your chrome browser.")
    raise SystemExit(1)


# fmt: off
# browser = LOOP.run_until_complete(get_ppbrowser(not HEADFUL))
async def deepl_tr_async(
        text: str,
        from_lang: str = "auto",
        to_lang: str = "auto",
        # headless: bool = not HEADFUL,
        debug: bool = False,
        # proxy: Optional[str] = None,
        waitfor: Optional[float] = None,
        browser=BROWSER,
) -> Optional[str]:
    """ deepl via pyppeteer
    from_lang = 'de'
    to_lang = 'en'
    debug = 1
    """

    # fmt: on

    if debug:
        logzero.loglevel(10)
    else:
        logzero.loglevel(20)
    if from_lang.lower() == "auto":
        try:
            # from_lang = langid.classify(text)[0]
            from_lang = Detector(text).languages[0].code
        except Exception as exc:
            # logger.error("langid.classify failed: %s, setting from_lang to en", exc)
            logger.error("polyglot.detect.Detector failed: %s, setting from_lang to en", exc)
            from_lang = "en"
    if to_lang == "auto":
        if from_lang not in ["en"]:
            to_lang = "en"
        else:
            to_lang = "de"

    langs = ["auto", "en", "de", "zh", "fr", "es", "pt", "it", "nl", "pl", "ru", "ja"]

    try:
        from_lang = from_lang.lower()
    except Exception as exc:
        from_lang = "en"
        logger.warning("%s", exc)
    try:
        to_lang = to_lang.lower()
    except Exception as exc:
        to_lang = "en"
        logger.warning("%s", exc)

    if from_lang not in langs:
        logger.warning(" from_lang [%s] not in the langs set, setting to en", from_lang)
        from_lang = "en"
    if to_lang not in langs:
        logger.warning(" to_lang [%s] not in the langs set, setting to en", to_lang)
        to_lang = "en"

    if from_lang == to_lang:
        logger.warning(
            " from_lang [%s] and to_lang [%s] are idnetical, nothing to do",
            from_lang,
            to_lang,
        )
        return text

    then = default_timer()
    count = 0
    while count < 3:
        count += 1
        try:
            page = await browser.newPage()
            break
        except Exception as exc:
            logger.error(" browser.newPage exc: %s, failed attempt: %s", exc, count)
            asyncio.sleep(0)
    else:
        # giving up
        return

    # set timeout to 45 s, default 30 s
    if HEADFUL:
        page.setDefaultNavigationTimeout(0)
    else:
        page.setDefaultNavigationTimeout(75000)

    url_ = f"{URL}#{from_lang}/{to_lang}/{quote(text)}"
    # url_ = f'{URL}#{from_lang}/{to_lang}/'

    # await page.type(".lmt__source_textarea", text + text + ' ' * 90)

    count = 0
    while count < 3:
        count += 1
        try:
            # await page.goto(url_)
            await page.goto(url_, {"timeout": 90 * 1000})
            # await page.goto(url_, {"timeout": 0})
            break
        except Exception as exc:
            asyncio.sleep(0)
            page = await browser.newPage()
            logger.warning("page.goto exc: %s, attempt %s", str(exc)[:100], count)
    else:
        # return
        raise Exception("Unable to fetch %s..." % url_[:20])

    # wait for input area ".lmt__source_textarea"
    try:
        # await page.waitFor(".lmt__message_box2__content")
        await page.waitForSelector(".lmt__source_textarea", {"timeout": 1000})  # ms
        logger.debug(" *** .lmt__source_textarea success")
    # except TimeoutError:
    except Exception as exc:
        if debug:
            logger.error("Timedout: %s, waiting for 500 ms more", exc)
            logger.error("text: %s", text)
        await asyncio.sleep(0.5)
        # raise

    logger.debug("page.goto(url_) time: %.2f s", default_timer() - then)
    then = default_timer()

    # .lmt__message_box2__content

    # await page.waitFor(2500)  # ms

    # wait for popup to be visible
    _ = """
    try:
        # await page.waitFor(".lmt__message_box2__content")
        await page.waitForSelector(".lmt__message_box2__content", {"timeout": 1000})  # ms
    # except TimeoutError:
    except Exception as exc:
        if debug:
            logger.error("Timedout: %s, waiting for 500 ms more", exc)
        await asyncio.sleep(0.5)
        # raise
    """

    # _ = int(min(10, len(text) * 0.2))
    # await page.type(".lmt__source_textarea", text + ' ' * _)

    if waitfor is None:
        _ = max(100, len(text) * 3.6)
        logger.debug("waiting for %.1f ms", _)
    else:
        try:
            _ = float(waitfor)
        except Exception as exc:
            logger.warning(
                " invalif waitfor [%s]: %s, setting to auto-adjust", waitfor, exc
            )
            _ = max(100, len(text) * 3.6)

        logger.debug("preset fixed waiting for %.1f ms", _)

    # ".lmt__translations_as_text"
    # await page.waitFor(".lmt__translations_as_text", {"timeout": _})  # ms

    # logger.debug(" is page closed? ")
    try:
        await page.waitFor(_)
    except Exception as exc:
        logger.warning(" page.waitFor exc: %s", exc)
    try:
        content = await page.content()
    except Exception as exc:
        logger.warning(" page.waitFor exc: %s", exc)
        content = '<div class="lmt__translations_as_text">%s</div>' % exc

    doc = pq(content)
    res = doc(".lmt__translations_as_text").text()

    count = -1
    while count < 50:
        count += 1
        logger.debug(" extra %s x 100 ms", count + 1)
        await page.waitFor(100)

        content = await page.content()
        doc = pq(content)
        res = doc(".lmt__translations_as_text").text()
        if res:
            break
        asyncio.sleep(0)
        asyncio.sleep(0)

    logger.debug("time: %.2f s", default_timer() - then)

    logger.debug("res: %s", res)

    if not debug:
        pass
    await page.close()

    asyncio.sleep(0.2)

    # copy('\n'.join(wrap(res, 45)))

    # logger.info('exit: %s', text[:200])

    return res


def deepl_mpages(  # pragrma: no cover
        sents: Union[str, List[str]],
        from_lang: str = "auto",
        to_lang: str = "auto",
        # headless: bool = not HEADFUL,
        debug: bool = False,
        waitfor: Optional[float] = None,
        loop=None,
        browser=BROWSER,
) -> Union[Tuple[Optional[str]], Any]:
    # ) -> List[Union[Optional[str], Any]]:
    """ multiple pages
    """

    if loop is None:
        loop = LOOP
    if loop.is_closed():
        loop = asyncio.new_event_loop()

    if isinstance(sents, str):
        sents = [sents]

    # browser = await get_ppbrowser(headless)
    tasks = (
        deepl_tr_async(
            elm,
            from_lang=from_lang,
            to_lang=to_lang,
            debug=debug,
            waitfor=waitfor,
            browser=browser,
        )
        for elm in sents
    )

    try:
        res = loop.run_until_complete(asyncio.gather(*tasks))
    except Exception as exc:
        logger.error(" loop.run_until_complete exc: %s", exc)
        res = str(exc)

    if not debug:
        pass
        # LOOP.run_until_complete(browser.close())

    return res


def main():
    """main"""
    # from time import sleep

    # pylint: disable=line-too-long
    text = """Die Rohstoffpreise sind abgestürzt, die Coronakrise trifft die Exportländer mit Wucht. Das Öl wird weiter gefördert, aber derzeit nicht gebraucht. Nun könnten einige Staaten in eine gefährliche Kreditklemme geraten."""

    text1 = """Im Westen Kanadas reißt die Ölindustrie tiefe Narben in die Landschaft. Dort bauen die Unternehmen Ölsande ab: Zwei Tonnen Material sind nötig, um eine Tonne Öl zu gewinnen. Es ist die wohl aufwendigste und dreckigste Art der Brennstoff-Produktion. Und gegenwärtig auch die unwirtschaftlichste."""

    # text2 = f"{text} {text1} "  # pylint: disable=unused-variable

    debug = DEBUG

    # _ = """
    then = default_timer()

    # browser = LOOP.run_until_complete(get_ppbrowser())
    # logger.info(" get_ppbrowser time: %.2f", default_timer() - then)

    # res = LOOP.run_until_complete(deepl_(text1, debug=debug))
    # res = LOOP.run_until_complete(deepl_("verramschen", debug=debug))
    res = deepl_mpages(["verramschen"], debug=debug)

    logger.info(" deepl_mpage 2a= %s", res)
    logger.info(" deepl_mpage 2a=== time: %.2f", default_timer() - then)
    # """

    # sleep(12)

    _ = """
    then = default_timer()
    coros = [
        # deepl_(text, debug=debug),
        deepl_(text, debug=debug),
        deepl_(text1, debug=debug),
        # deepl_(text1, to_lang="", debug=debug),
        # deepl_("verramschen", debug=debug),
        # deepl_("verramschen", to_lang="zh", debug=debug),
        # deepl_("sell off", to_lang="zh", debug=debug),
        # deepl_("sell off", to_lang="fr", debug=debug),
    ]
    res12 = LOOP.run_until_complete(asyncio.gather(*coros))
    logger.info(" 3== %s", res12)
    logger.info(' 3==== time: %.2f', default_timer() - then)
    # """

    then = default_timer()
    # browser = LOOP.run_until_complete(get_ppbrowser())
    # logger.info(" -- get_ppbrowser time: %.2f", default_timer() - then)

    res12 = deepl_mpages(
        ["verramschen", "verramschen", text, text1, text1, text1], debug=debug
    )
    logger.info(" deepl_mpage 3== %s", res12)
    logger.info(" deepl_mpage 3==== time: %.2f", default_timer() - then)


# pylint: disable=invalid-name
if __name__ == "__main__":
    main()
