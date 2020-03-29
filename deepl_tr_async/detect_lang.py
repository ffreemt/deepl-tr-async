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


# pragrma: no cover
def test_en():
    """
    test en
    """

    text = "This is an English test "
    text = """There is some concern that unifying the Han characters may lead to confusion because they are sometimes used differently by the various East Asian languages. Computationally, Han character unification presents no more difficulty than employing a single Latin character set that is used to write languages as different as English and French. Programmers do not expect the characters “c”, “h”, “a”, and “t” alone to tell us whether chat is a French word for cat or an English word meaning “informal talk.” Likewise, we depend on context to identify the American hood (of a car) with the British bonnet. Few computer users are confused by the fact that ASCII can also be used to represent such words"""  # NOQA
    # eq_('english', detect_lang(text))
    assert detect_lang(text) == "en"
    assert detect_lang(text, 1) == "english"

    text = """Forum libre! Discutez de n'importe quoi en français.
        Chat about anything you'd like, en français.
        """
    text = """Forum libre! Discutez de n'importe quoi en français.
        en français.
        """
    # eq_('french', detect_lang(text))
    assert "fr" == detect_lang(text)
    assert "french" == detect_lang(text, 1)

    text = "Ogni individuo ha diritto all'istruzione. L'istruzione deve essere gratuita almeno per quanto riguarda le classi elementari e fondamentali. L'istruzione elementare deve essere obbligatoria. L'istruzione tecnica e professionale deve essere messa alla portata di tutti e l'istruzione superiore deve essere egualmente accessibile a tutti sulla base del merito."  # NOQA
    # eq_('italian', detect_lang(text))
    assert "it" == detect_lang(text)
    assert "italian" == detect_lang(text, 1)

    text = "auf deutsch"
    # eq_('german', detect_lang(text))
    assert "de" == detect_lang(text)
    assert "german" == detect_lang(text, 1)


def test_zh():
    """
    test zh
    """
    text = """人类学家说，只有一个生物常数：女的在所有的社会角色，包括轴承、儿童和初级保健护理。否则，几乎任何事情–只要去找女人的一种方式和其他人。
【吐槽】sky (2931712793) 19:40:17"""

    # eq_('chinese', detect_lang(text))
    assert "zh" == detect_lang(text)
    assert "chinese" == detect_lang(text, 1)


def test_pt():
    """
    test portuguese
    """
    text = """	O Brasil é um país que sempre foi referido por outras nações por seu tamanho ou por sua população. Mas em discussões entre os cientistas, jornalistas, economistas, e experientes internacionais, este país é muitas vezes caracterizado como um país subdesenvolvido."""  # NOQA

    # eq_('portuguese', detect_lang(text))
    assert "pt" == detect_lang(text)
    assert "portuguese" == detect_lang(text, 1)


def test_es():
    """
    test spanish
    """
    text = """	Es un área definida de la superficie, ya sea de tierra, agua o hielo propuesto para la llegada, salida y movimiento en superficie de aeronaves de distintos tipos con llegadas y salidas nacionales e internacionales. """  # NOQA

    # eq_('spanish', detect_lang(text))
    assert "es" == detect_lang(text)
    assert "spanish" == detect_lang(text, 1)
