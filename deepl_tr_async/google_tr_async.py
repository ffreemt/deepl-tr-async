"""

modified from deepl_tr_async

googlecn:
de-zh zh-CN
f"https://translate.google.cn/#view=home&op=translate&sl=de&tl=de&text={text}"

en-zh zh-CN
https://translate.google.cn/#view=home&op=translate&sl=zh-CN&tl=de&text={text}"

.result-shield-container
pq(content)(".result-shield-container").text()

async fetch(url, css, browser=None):

"""
# pylint: disable=too-many-arguments, too-many-locals
# pylint: disable=too-many-statements, too-many-branches
# pylint: disable=unused-import

from typing import Any, List, Optional, Tuple, Union

# import os
import asyncio
from timeit import default_timer
from urllib.parse import quote

from pyquery import PyQuery as pq
# import dotenv

from polyglot.detect import Detector
import logzero
from logzero import logger
# from environs import Env

from deepl_tr_async import BROWSER, get_ppbrowser, HEADFUL, DEBUG
from deepl_tr_async.google_langpair import google_langpair

URL = r"https://translate.google.cn/#view=home&op=translate&"
# if not LOOP.is_closed(): LOOP = asyncio.new_event_loop()

LOOP = asyncio.get_event_loop()

# dotenv.load_dotenv(verbose=1)
# in shell or in .env
# set HEADFUL=anything (include 0 False) to show browser

_ = """\
ENV = Env()
_ = dotenv.find_dotenv()
if _:
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
logger.info(" HEADFUL: %s", HEADFUL)
logger.info(" DEBUG: %s", DEBUG)
# """


# fmt: off
async def google_tr_async(
        text: str,
        from_lang: str = "auto",
        to_lang: str = "auto",
        # headless: bool = not HEADFUL,
        debug: bool = False,
        # proxy: Optional[str] = None,
        waitfor: Optional[float] = None,
        browser=BROWSER,
) -> Optional[str]:
    """ google via pyppeteer
    from_lang = 'de'
    to_lang = 'en'
    debug = 1
    waitfor: Optional[float] = None
    browser=BROWSER
    """

    # browser = await get_ppbrowser(headless)

    # fmt: on

    if debug:
        logzero.loglevel(10)
    else:
        logzero.loglevel(20)
    if from_lang.lower() == "auto":
        try:
            # from_lang = langid.classify(text)[0]
            from_lang = Detector(text).language.code
        except Exception as exc:
            # logger.error("langid.classify failed: %s, setting from_lang to en", exc)
            logger.error("polyglot.detect.Detector failed: %s, setting from_lang to en", exc)
            from_lang = "en"
    if to_lang == "auto":
        if from_lang not in ["en"]:
            to_lang = "en"
        else:
            to_lang = "de"

    # langs = ["auto", "en", "de", "zh", "fr", "es", "pt", "it", "nl", "pl", "ru", "ja"]

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

    _ = """
    if from_lang not in langs:
        logger.warning(" from_lang [%s] not in the langs set, setting to en", from_lang)
        from_lang = "en"
    if to_lang not in langs:
        logger.warning(" to_lang [%s] not in the langs set, setting to en", to_lang)
        to_lang = "en"
    # """

    logger.debug("langpair: %s, %s", from_lang, to_lang)
    from_lang, to_lang = google_langpair(from_lang, to_lang)
    logger.debug("converted langpair: %s, %s", from_lang, to_lang)

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
            browser = await get_ppbrowser(not HEADFUL)
            asyncio.sleep(0)
    else:
        # giving up
        logger.warning("Unable to make newPage work...")
        raise Exception("Unable to get newPage work, giving up...")

    # set timeout, default is 30 s
    _ = """\
    if HEADFUL:
        page.setDefaultNavigationTimeout(0)
    else:
        page.setDefaultNavigationTimeout(75000)
    # """

    page.setDefaultNavigationTimeout(75000)

    # url_ = f'{URL}#{from_lang}/{to_lang}/'
    # url_ = f"{URL}#{from_lang}/{to_lang}/{quote(text)}"

    # sl=de&tl=de&text={text}
    url_ = f"{URL}sl={from_lang}&tl={to_lang}&text={quote(text)}"

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
        logger.error("Unable to fetch %s...", url_[:20])
        raise Exception("Unable to fetch %s..." % url_[:20])

    # wait for input area ".lmt__source_textarea"
    # wait for input area ".result-shield-container"
    try:
        # await page.waitFor(".lmt__message_box2__content")
        await page.waitForSelector(".result-shield-container", {"timeout": 1000})  # ms
        logger.debug(" *** .result-shield-container")
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
        content = '<div class=".result-shield-container">%s</div>' % exc

    doc = pq(content)
    res = doc(".result-shield-container").text()

    count = -1
    while count < 50:
        count += 1
        logger.debug(" extra %s x 100 ms", count + 1)
        await page.waitFor(100)

        content = await page.content()
        doc = pq(content)
        res = doc(".result-shield-container").text()
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


def google_mpages(  # pragrma: no cover
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

    if loop is None:  # pragrma: no cover
        loop = LOOP
    # if loop.is_closed(): loop = asyncio.new_event_loop()

    if isinstance(sents, str):
        sents = [sents]

    tasks = (
        google_tr_async(
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
    res = LOOP.run_until_complete(google_tr_async(text, debug=debug))
    logger.info(" 1= %s", res)
    logger.info('1=== time: %.2f', default_timer() - then)
    # """

    # sleep(5)

    # _ = """
    then = default_timer()

    # br = LOOP.run_until_complete(get_ppbrowser(1))
    res = LOOP.run_until_complete(google_tr_async(text1, debug=debug))
    logger.info(" 2= %s", res)
    logger.info(' 2=== time: %.2f', default_timer() - then)
    # """
    # sleep(12)

    # _ = """
    then = default_timer()

    # browser = LOOP.run_until_complete(get_ppbrowser())
    # logger.info(" get_ppbrowser time: %.2f", default_timer() - then)

    # res = LOOP.run_until_complete(google_(text1, debug=debug))
    # res = LOOP.run_until_complete(google_("verramschen", debug=debug))
    res = google_mpages(["verramschen"], debug=debug)

    logger.info(" google_mpage 2a= %s", res)
    logger.info(" google_mpage 2a=== time: %.2f", default_timer() - then)
    # """

    # sleep(12)

    _ = """
    then = default_timer()
    coros = [
        # google_(text, debug=debug),
        google_(text, debug=debug),
        google_(text1, debug=debug),
        # google_(text1, to_lang="", debug=debug),
        # google_("verramschen", debug=debug),
        # google_("verramschen", to_lang="zh", debug=debug),
        # google_("sell off", to_lang="zh", debug=debug),
        # google_("sell off", to_lang="fr", debug=debug),
    ]
    res12 = LOOP.run_until_complete(asyncio.gather(*coros))
    logger.info(" 3== %s", res12)
    logger.info(' 3==== time: %.2f', default_timer() - then)
    # """

    then = default_timer()
    # browser = LOOP.run_until_complete(get_ppbrowser())
    # logger.info(" -- get_ppbrowser time: %.2f", default_timer() - then)

    res12 = google_mpages(
        ["verramschen", "verramschen", text, text1, text1, text1], debug=debug
    )
    logger.info(" google_mpage 3== %s", res12)
    logger.info(" google_mpage 3==== time: %.2f", default_timer() - then)


# pylint: disable=invalid-name
if __name__ == "__main__":
    main()
