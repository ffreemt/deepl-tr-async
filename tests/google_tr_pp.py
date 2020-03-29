r"""
google translate via deepl_tr_async (pypputeer)

"""
from typing import List, Optional, Union

import asyncio
import re
from .limited_as_completed import limited_as_completed
from linetimer import CodeTimer as timeme
from logzero import logger

from deepl_tr_async.google_tr_async import google_tr_async

# Optional[str]

LOOP = asyncio.get_event_loop()


# fmt: off
def google_tr_pp(
        text: Union[str, List[str]],
        from_lang: str = "auto",
        to_lang: str = "zh",
        debug: bool = False,
) -> List[Optional[str]]:
    # fmt: on
    """

    from_lang = "auto"
    to_lang = "zh"
    debug = False
    """

    if isinstance(text, str):
        text = [text]

    # replace % with _c_
    text = [elm.replace("%", "_c_").strip() for elm in text if elm.strip()]

    # tasks = (google_tr_async(elm, from_lang=from_lang, to_lang=to_lang) for elm in text)

    futures = [asyncio.ensure_future(google_tr_async(elm, from_lang=from_lang, to_lang=to_lang)) for elm in text]
    # record positions
    fut_index = dict((fut, idx) for idx, fut in enumerate(futures))

    try:
        # _ = asyncio.gather(*tasks)
        # res = LOOP.run_until_complete(_)
        # res = [*limited_as_completed(tasks, limit=limit)]
        # res = [*limited_as_completed(tasks)]
        res = [*limited_as_completed(iter(futures), 3)]
        # order not preserved

    except Exception as exc:
        logger.error(" LOOP.run_until_complete exc: %s", exc)
        res = [str(exc)]
        return res

    # reorder

    # return [res[fut_index[fut]] for fut in futures]
    res = [fut.result() for fut in futures]

    res = [elm.replace("_c_", "%").strip() for elm in res if elm.strip()]

    # remove spaces after ([，。！？])\s+([一-龥])
    res = [re.sub(r"([，。！？])\s+([一-龥])", r"\1\2", elm) for elm in res]

    return res


# def test_sanity(capsys):
def test_sanity():
    """ test auto zh """
    text = "this is a normal test."

    with timeme():
        res = google_tr_pp(text)
    # ['这是正常测试。']

    logger.info(res)
    # with capsys.disabled():
    print("pr", res)

    assert "测试" in res[0]


def test_paras():
    """ test auto zh """
    text = """\
The return value from readouterr changed to a namedtuple with two attributes, out and err.

If the code under test writes non-textual data, you can capture this using the capsysbinary fixture which instead returns bytes from the readouterr method. The capfsysbinary fixture is currently only available in python 3.

If the code under test writes non-textual data, you can capture this using the capfdbinary fixture which instead returns bytes from the readouterr method. The capfdbinary fixture operates on the filedescriptor level.
"""
    text = [elm.strip() for elm in text.splitlines() if elm.strip()]
    with timeme():
        res = google_tr_pp(text)

    logger.info(res)
    # with capsys.disabled():
    # print("pr", res)

    assert "返回值" in res[0]
    assert "3" in res[1]
