"""

in mypython
Detect language using longid.classify.

detct as Chinese if chinese_char_ratio>= threthold else dectect_language()

"""

# from detect_language import detect_language
# from langdetect import detect
# import langid
# from chinese_char_ratio import chinese_char_ratio

from typing import Union
from polyglot.detect import Detector

from logzero import logger as LOGGER


# def detect_lang(text1, threthold=0.1, checklen=3000):
# def detect_lang(text1, checklen=3000, langs=None):
# def detect_lang(text1, checklen=3000):
def detect_lang(text1: str, name: Union[bool, int] = False) -> str:
    """
    return name.lower() if name is True

    Detect Chinese and other languages using polyglot.
    """

    if not text1.strip():
        detected = "en"
        if name:
            detected = "english"
    else:
        try:
            # detected = Detector(text1).languages[0].code
            _ = Detector(text1).language
            if name:
                detected = _.name.lower()
            else:
                detected = _.code
        except Exception as exc:
            # LOGGER.debug(" langid.classify failed: %s", exc)
            LOGGER.debug(
                " Detector(text1).language[0] failed: %s, setting to 'en'/'english' ",
                exc,
            )
            if name:
                detected = "english"
            else:
                detected = "en"

    return detected
