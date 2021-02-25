""" test deelp """
import asyncio

# import pytest
from logzero import logger
import warnings

from deepl_tr_async import __version__

# from deepl_tr_async.deepl_tr_async import deepl_tr_async
# from deepl_tr_async import deepl_tr_async
from deepl_tr_async.google_tr_async import google_tr_async

warnings.filterwarnings("ignore", ".*pure-python.*")  # regex

LOOP = asyncio.get_event_loop()


def test_version():
    assert __version__[:4] == "0.0."


# @pytest.mark.asyncio
def test_google_en_zh(caplog):
    """ test_google_en_zh"""

    text = "test this and that"
    # res = await deepl_tr_async(text)
    # res = LOOP.run_until_complete(deepl_tr_async(text, to_lang="zh"))
    res = LOOP.run_until_complete(google_tr_async(text, to_lang="zh"))
    logger.info(" res: %s", res)

    with caplog.at_level(20):  # caplog.text
        logger.debug("test_google_en_zh res: %s", res)
    assert all(map(lambda elm: elm in res, "测试个"))


def test_google_en_de():
    """ test_google_en_de"""

    text = "test this and that"
    # res = await deepl_tr_async(text)
    # res = LOOP.run_until_complete(deepl_tr_async(text, to_lang="de"))
    res = LOOP.run_until_complete(google_tr_async(text, to_lang="de"))
    logger.info(" res: %s", res)

    assert res.lower() == "teste dies und das"

    # pytest -s to show log in this file
