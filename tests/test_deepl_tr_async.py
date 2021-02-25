""" test deelp """
import asyncio
import pytest
from logzero import logger

from deepl_tr_async import __version__
# from deepl_tr_async.deepl_tr_async import deepl_tr_async
from deepl_tr_async import deepl_tr_async

LOOP = asyncio.get_event_loop()

def test_version():
    logger.info("\n\t version: %s", __version__)
    assert __version__[:4] == '0.0.'

# @pytest.mark.asyncio
# --show-capture: invalid choice: 'yes' (choose from 'no', 'stdout', 'stderr', 'log', 'all')
# -s show normal print/logger.info/debug output
def test_deepl_en_zh(caplog):
    """ test_deepl_en_zh"""

    text = "test this and that"

    text1 = "A dedicate website will go live in January and the Task Force has planned a two to three-month sprint to kick start its work."
    exp1 = "专门网站将于1月上线，工作队计划用两到三个月的时间冲刺，以启动其工作。"

    res = LOOP.run_until_complete(deepl_tr_async(text, to_lang="zh"))
    # res = await deepl_tr_async(text)
    # with caplog.at_level(20):
    with caplog.at_level(10):
        # logger.info("test_deepl_en_zh res: %s", res)
        logger.info("test_deepl_en_zh res: %s", res)
        logger.info("caplog.text: %s", caplog.text)
        # pytest -s

    _ = ["测验", "试探", "检验"]
    assert any(map(lambda elm: elm in res, _))
