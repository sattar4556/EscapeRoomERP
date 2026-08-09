import logging

from pathlib import Path


LOG_DIR = Path(

    "logs"

)

LOG_DIR.mkdir(

    exist_ok=True,

)


LOG_FILE = LOG_DIR / "bot.log"


logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s | %(levelname)s | %(message)s",

    handlers=[

        logging.FileHandler(

            LOG_FILE,

            encoding="utf-8",

        ),

        logging.StreamHandler(),

    ],

)


logger = logging.getLogger(

    "EscapeRoomERP"

)


def info(

    message,

):

    logger.info(

        message,

    )


def warning(

    message,

):

    logger.warning(

        message,

    )


def error(

    message,

):

    logger.error(

        message,

    )


def critical(

    message,

):

    logger.critical(

        message,

    )


def exception(

    message,

):

    logger.exception(

        message,

    )
