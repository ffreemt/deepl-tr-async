'''
deepl.com fanyi code

based on you dao_langpair.py
'''
import logging
import pytest
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())
OTHER_CODES = ['zh_cn', 'ja', 'kr', 'ru', 'vi', 'zh', ]
DEEPLTR_CODES = ['auto', 'en', 'de', 'fr', 'it', 'pl', 'es', 'nl']

OTHER_CODES = ['kr', 'vi', ]
DEEPLTR_CODES = ['auto', 'zh', 'ja', 'ru', 'en', 'de',
                 'fr', 'it', 'pl', 'es', 'nl', 'pt']


class InvalidPair(Exception):
    '''in valid pair if
    src_lang not in DEEPLTR_CODES or src_lang not in DEEPLTR_CODES
        (not (src_lang not in DEEPLTR_CODES and src_lang in DEEPLTR_CODES))
    '''
    pass


def deepl_langpair(srclang, tgtlang):
    '''
    convert srclang, tgtlang to a pair suitable for deepl fanyi
    '''
    # LOGGER.debug(" inp: %s, %s", srclang, tgtlang)

    try:
        srclang = srclang.lower().strip()
    except Exception as exc:
        LOGGER.warning(exc)
        srclang = ''

    # LOGGER.debug(" inp: %s, %s", srclang, tgtlang)

    try:
        tgtlang = tgtlang.lower().strip()
    except Exception as exc:
        LOGGER.warning(exc)
        tgtlang = ''

    if srclang in ['chinese', 'zhong', 'cn']:
        srclang = 'zh'
    if tgtlang in ['chinese', 'zhong', 'cn']:
        tgtlang = 'zh'

    if srclang == '':
        srclang = 'auto'
    if tgtlang == '':
        tgtlang = 'auto'

    # LOGGER.debug(" inp0: %s, %s", srclang, tgtlang)

    if srclang == 'auto' and tgtlang == 'auto':
        tgtlang = 'en'

    # LOGGER.debug(" inp1: %s, %s", srclang, tgtlang)

    if srclang != 'auto' and srclang != 'en' and tgtlang == 'auto':
        tgtlang = 'en'

    if srclang == 'en' and tgtlang == 'auto':
        tgtlang = 'de'

    if srclang in ['eng', 'english', 'en-US', ]:
        srclang = 'en'
    if tgtlang in ['eng', 'english', 'en-US', ]:
        tgtlang = 'en'

    # LOGGER.debug('out: %s, %s', srclang, tgtlang)

    if srclang not in DEEPLTR_CODES:
        src_score = process.extractOne(srclang, DEEPLTR_CODES + OTHER_CODES, scorer=fuzz.UWRatio)
        # srclang0 = srclang
        srclang = src_score[0]

        # LOGGER.warning(" %s not recognized, guessing to be %s ", srclang0, srclang)

    if tgtlang not in DEEPLTR_CODES:
        tgt_score = process.extractOne(tgtlang, DEEPLTR_CODES + OTHER_CODES, scorer=fuzz.UWRatio)
        # tgtlang0 = tgtlang
        tgtlang = tgt_score[0]
        # LOGGER.warning(" %s not recognized, guessing to be %s ", tgtlang0, tgtlang)

    if (srclang not in DEEPLTR_CODES) or (tgtlang not in DEEPLTR_CODES):
        msg = 'The pair {} is not valid.'
        msg = msg.format((srclang, tgtlang))
        raise InvalidPair(msg)

    return srclang, tgtlang


@pytest.mark.parametrize(
    "inpair, outpair", [
        (('auto', 'auto'), ('auto', 'en')),
        (('en', 'auto'), ('en', 'de')),
        (('de', 'auto'), ('de', 'en')),
        (('', 'auto'), ('auto', 'en')),
        (('', ''), ('auto', 'en')),
        (('en', ''), ('en', 'de')),
        ((1, ''), ('auto', 'en')),  # srclang strip() exception ==> '' >> 'auto'
        (('', 1), ('auto', 'en')),  # tgtlan strip() exception ==> '' >> 'auto'
        # (('en', 'cn'), ('en', 'zh_ cn')),
        # (('chinese', 'en'), ('zh_ cn', 'en')),
        # process.extractOne("enn", DEEPLTR_CODES, scorer=fuzz.UWRatio)
        # (('chinese', 'enn'), ('zh_ cn', 'en')),
        (('enn', 'de'), ('en', 'de')),
        (('enn', 'De'), ('en', 'de')),
        (('eng', 'De'), ('en', 'de')),
        (('de', 'english'), ('de', 'en')),
    ]
)
def test_pairs(inpair, outpair, caplog):
    '''test_pairs'''
    caplog.set_level(logging.DEBUG)
    msg = 'inp: {}, {} != {}'
    out = deepl_langpair(*inpair)
    msg = msg.format(inpair, out, outpair)
    assert out == outpair, msg


@pytest.mark.parametrize(
    "inpair, outpair", [
        (('en', 'cn'), ('en', 'zh')),
        (('chinese', 'en'), ('zh', 'en')),
        (('chinese', 'enn'), ('zh', 'en')),
        (('eng', 'zh'), ('en', 'zh')),
        (('zh-cn', 'english'), ('zh', 'en')),
    ]
)
def test_pairs_zh(inpair, outpair, caplog):
    '''test_pairs'''
    caplog.set_level(logging.DEBUG)
    msg = 'inp: {}, {} != {}'
    out = deepl_langpair(*inpair)
    msg = msg.format(inpair, out, outpair)
    assert out == outpair, msg


@pytest.mark.xfail(raises=InvalidPair)
def test_invalid_enko():
    '''invalid pair en ko'''
    srclang = 'en'
    tgtlang = 'ko'
    deepl_langpair(srclang, tgtlang)


@pytest.mark.xfail(raises=InvalidPair)
def test_invalid_zhen():
    '''invalid pair zh en'''
    srclang = 'zh'
    tgtlang = 'en'
    deepl_langpair(srclang, tgtlang)
