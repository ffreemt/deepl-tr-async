r""" deepl translate via pyppeteer
for de/fr/ja/it/x as third language
"""
import asyncio
import pyperclip
from absl import app, flags
from textwrap import fill
import logzero
from logzero import logger

from deepl_tr_async.deepl_tr_async import main, LOOP
from deepl_tr_async import deepl_tr_async
from deepl_tr_async.google_tr_async import google_tr_async
from deepl_tr_async.detect_lang import detect_lang

FLAGS = flags.FLAGS
flags.DEFINE_string(
    'z-extra-info',
    'info',
    'supply text anywhere in the command line when --copyfrom=false',
)
flags.DEFINE_string(
    # 'from-lang',
    'mother-lang',
    'zh',
    'mother tongue language, default chinese)',
    short_name='m'
)
flags.DEFINE_string(
    # 'to-lang',
    'second-lang',
    'en',
    'second language, default english',
    short_name='s'
)
flags.DEFINE_string(
    # 'to-lang',
    'third-lang',
    'de',
    'third language, defaut german',
    short_name='t'
)

flags.DEFINE_integer("width", 60, "display width", short_name='w')
flags.DEFINE_boolean('copyto', True, 'copy thre result to clipboard')
flags.DEFINE_boolean('copyfrom', True, 'copy from clipboard, default true (input taken fomr the terminal if false)')
flags.DEFINE_boolean('debug', False, 'print debug messages.')
flags.DEFINE_boolean('version', False, 'print version and exit')

# FLAGS(shlex.split("app --from-lang=en"))


# def main(argv):
def proc_argv(argv):
    """ __main__ main """

    version = "0.0.2"
    if FLAGS.version:
        print("deepl-tr-async %s" % version)

    if FLAGS.copyfrom:
        text = pyperclip.paste()
        logger.debug("text from clipboard: %s", text)
    else:
        text = ' '.join(argv[1:])
        logger.debug("argv from terminal: %s", text)

    try:
        text = text.strip()
    except Exception as exc:
        logger.warning("text.strip() exc: %s, exiting...", exc)
        text = ""

    if not text:
        return None

    # del argv

    if FLAGS.debug:
        logzero.loglevel(10)  # logging.DEBUG
    else:
        logzero.loglevel(20)  # logging.INFO

    logger.debug('\n\t args: %s', dict((elm, getattr(FLAGS, elm)) for elm in FLAGS))

    # to_lang = FLAGS.to_lang
    # from_lang = FLAGS.from_lang

    # to_lang = getattr(FLAGS, "to-lang")
    # from_lang = getattr(FLAGS, "from-lang")
    # width = getattr(FLAGS, "width")
    # copyto = getattr(FLAGS, "copyto")
    # debug = getattr(FLAGS, "debug")

    args = ['lang0', 'lang1', 'lang2', 'width'
            'copyfrom', 'copyto', 'debug', ]
    # for elm in args: locals()[elm] = getattr(FLAGS, elm)
    lang0 = getattr(FLAGS, "mother-lang")
    lang1 = getattr(FLAGS, "second-lang")
    lang2 = getattr(FLAGS, "third-lang")
    width = FLAGS.width
    # copyfrom = FLAGS.copyfrom
    copyto = FLAGS.copyto
    debug = FLAGS.debug

    # if getattr(FLAGS, "debug"):
    if debug:
        logger.debug("args: %s", [[elm, getattr(FLAGS, elm)] for elm in args])

    # make it unique and not the same as s_lang
    s_lang = detect_lang(text)
    logger.info(" detected language: %s", s_lang)

    lang_list = []
    for elm in [lang0, lang1, lang2]:
        if elm not in lang_list and elm not in [s_lang]:
            lang_list.append(elm)

    if not lang_list:
        logger.info(" languages picked: %s", [lang0, lang1, lang2])
        logger.warning(" Nothing to do. Select proper languages and source text and try again, exiting... ...")
        return None

    if len(lang_list) < 2:
        logger.warning(" Only one language %s is selected. We'll proceed tho.", lang_list)

    tasks = []
    for elm in lang_list:
        task = deepl_tr_async(
            text,
            from_lang=s_lang,
            to_lang=elm
        )
        tasks.append(task)

    # google tr
    tasks_g = []
    for elm in lang_list:
        task = google_tr_async(
            text,
            from_lang=s_lang,
            to_lang=elm
        )
        tasks_g.append(task)

    len_ = len(tasks)
    try:
        # trtext = LOOP.run_until_complete(task)
        _ = asyncio.gather(*tasks, *tasks_g)
        trtext_ = LOOP.run_until_complete(_)
    except Exception as exc:
        logger.error("LOOP.run_until_complete exc: %s", exc)
        trtext_ = [str(exc)] * len_

    trtext, trtext_g = trtext_[:len_], trtext_[len_:]

    prefix = " deepl: "
    indent = ' ' * len(prefix)
    ftext = prefix
    for elm in trtext:
        if detect_lang(elm) in ['zh', 'ja']:
            ftext += fill(elm, width // 2, subsequent_indent=indent) + "\n"
        else:
            ftext += fill(elm, width, initial_indent=indent, subsequent_indent=indent) + "\n"

    prefix = " google: "
    indent = ' ' * len(prefix)
    ftext_g = prefix
    for elm in trtext_g:
        if detect_lang(elm) in ['zh', 'ja']:
            ftext_g += fill(elm, width // 2, subsequent_indent=indent) + "\n"
        else:
            ftext_g += fill(elm, width, initial_indent=indent, subsequent_indent=indent) + "\n"

    prefix = " deepl: "
    indent = ' ' * len(prefix)
    if detect_lang(text) in ['zh', 'ja']:
        text_ = fill(text, width // 2, initial_indent=indent, subsequent_indent=indent) + "\n"
    else:
        text_ = fill(text, width, initial_indent=indent, subsequent_indent=indent) + "\n"

    _ = text_ + ftext + ftext_g

    if copyto:
        pyperclip.copy(_)

    logger.info("translated to %s: \n\t%s", ', '.join(lang_list), _)


def main():  # noqa: F811
    app.run(proc_argv)


if __name__ == "__main__":
    # app.run(main)
    main()
