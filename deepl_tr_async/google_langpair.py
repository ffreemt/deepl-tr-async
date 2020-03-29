'''
google fanyi code

https://cloud.google.com/translate/docs/languages
'''
import logging
import pytest
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

# BD_CODES = ['auto', 'zh', 'en', 'yue', 'wyw', 'jp', 'kor', 'fra', 'spa', 'th', 'ara', 'ru', 'pt', 'de', 'it', 'el', 'nl', 'pl', 'bul', 'est', 'dan', 'fin', 'cs', 'rom', 'slo', 'swe', 'hu', 'cht', 'vie']  # NOQA # pylint: disable=C0301
GOOGLETR_CODES = ['auto', 'af', 'sq', 'am', 'ar', 'hy', 'az', 'eu', 'be', 'bn', 'bs', 'bg', 'ca', 'ceb', 'zh-CN', 'zh-TW', 'hr', 'cs', 'da', 'nl', 'en', 'eo', 'et', 'fi', 'fr', 'fy', 'gl', 'ka', 'de', 'el', 'gu', 'ht', 'ha', 'haw', 'iw', 'hi', 'hmn', 'hu', 'is', 'ig', 'id', 'ga', 'it', 'ja', 'jw', 'kn', 'kk', 'km', 'ko', 'ku', 'ky', 'lo', 'la', 'lv', 'lt', 'lb', 'mk', 'mg', 'ms', 'ml', 'mt', 'mi', 'mr', 'mn', 'my', 'ne', 'no', 'ny', 'ps', 'fa', 'pl', 'pt', 'pa', 'ro', 'ru', 'sm', 'gd', 'sr', 'st', 'sn', 'sd', 'si', 'sk', 'sl', 'so', 'es', 'su', 'sw', 'sv', 'tl', 'tg', 'ta', 'te', 'th', 'tr', 'uk', 'ur', 'uz', 'vi', 'cy', 'xh', 'yi', 'yo', 'zu', ]


def google_langpair(srclang, tgtlang):
    '''
    convert srclang, tgtlang to a pair suitable for google fanyi
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

    if srclang == '':
        srclang = 'auto'
    if tgtlang == '':
        tgtlang = 'auto'

    # LOGGER.debug(" inp0: %s, %s", srclang, tgtlang)

    if srclang == 'auto' and tgtlang == 'auto':
        tgtlang = 'zh-CN'

    # LOGGER.debug(" inp1: %s, %s", srclang, tgtlang)

    if srclang != 'auto' and tgtlang == 'auto':
        tgtlang = 'zh-CN'

    if srclang in ['cn', 'chinese', 'zhong', 'zhongwen']:
        srclang = 'zh-CN'
    if tgtlang in ['cn', 'chinese', 'zhong', 'zhongwen']:
        tgtlang = 'zh-CN'

    # LOGGER.debug('out: %s, %s', srclang, tgtlang)

    if srclang not in GOOGLETR_CODES:
        src_score = process.extractOne(srclang, GOOGLETR_CODES, scorer=fuzz.UWRatio)
        srclang0 = srclang
        srclang = src_score[0]

        # LOGGER.warning(" %s not recognized, guessing to be %s ", srclang0, srclang)

    if tgtlang not in GOOGLETR_CODES:
        tgt_score = process.extractOne(tgtlang, GOOGLETR_CODES, scorer=fuzz.UWRatio)
        tgtlang0 = tgtlang
        tgtlang = tgt_score[0]
        # LOGGER.warning(" %s not recognized, guessing to be %s ", tgtlang0, tgtlang)

    return srclang, tgtlang


@pytest.mark.parametrize(
    "inpair, outpair", [
        (('auto', 'auto'), ('auto', 'zh-CN')),
        (('en', 'auto'), ('en', 'zh-CN')),
        (('', ''), ('auto', 'zh-CN')),
        (('en', ''), ('en', 'zh-CN')),
        ((1, ''), ('auto', 'zh-CN')),  # srclang strip() exception ==> '' >> 'auto'
        (('', 1), ('auto', 'zh-CN')),  # tgtlan strip() exception ==> '' >> 'auto'
        (('en', 'cn'), ('en', 'zh-CN')),
        (('EN', 'cn'), ('en', 'zh-CN')),
        (('EN', 'Cn'), ('en', 'zh-CN')),
        (('chinese', 'en'), ('zh-CN', 'en')),
        (('chinese', 'En'), ('zh-CN', 'en')),
        # process.extractOne("enn", GOOGLETR_CODES, scorer=fuzz.UWRatio)
        (('chinese', 'enn'), ('zh-CN', 'en')),
        (('enn', 'chinese'), ('en', 'zh-CN')),
        (('enn', 'zh TW'), ('en', 'zh-TW')),
    ]
)
def test_pairs(inpair, outpair, caplog):
    '''test_pairs'''
    caplog.set_level(logging.DEBUG)
    assert google_langpair(*inpair) == outpair
