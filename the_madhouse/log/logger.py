import logging, pathlib, os, re

from datetime import datetime
from logging.handlers import RotatingFileHandler
from paste.translogger import TransLogger


class AppLogger:
    @staticmethod
    def set_up_logger(level: int, filename: pathlib.Path):
        root_logger = logging.getLogger()
        root_logger.handlers = []
        root_file_handlers = [
            RotatingFileHandler(
                filename=filename,
                mode="a",
                maxBytes=20000,
                backupCount=10,
            ),
            logging.StreamHandler(),
        ]
        for handler in root_file_handlers:
            handler.setLevel(level=level)
            handler.setFormatter(
                fmt=logging.Formatter(
                    fmt="%(asctime)s - [%(levelname)s] [%(module)s] [%(name)s] - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                )
            )
        logging.basicConfig(level=level, handlers=root_file_handlers)
        for logger_name in logging.root.manager.loggerDict:
            logger = logging.getLogger(name=logger_name)
            logger.handlers = []
            logger.setLevel(level=level)

    @staticmethod
    def archive_logs(mode: str):
        pattern = rf"^{mode}log\.txt\..*$"
        try:
            for filename in os.listdir(path=pathlib.Path("./log")):
                if re.search(pattern=pattern, string=filename):
                    new_filename = re.sub(pattern=r"\.[^.]*$", repl="", string=filename)
                    os.rename(
                        src=pathlib.Path("./log") / filename,
                        dst=(
                            pathlib.Path("./log/archived/")
                            / f"{datetime.now().strftime(format='%Y%m%d_%H%M%S')}_{new_filename}"
                        ),
                    )
        except OSError as e:
            print(e.strerror)

    @staticmethod
    def set_up_translogger(app):
        return TransLogger(
            app,
            logger=logging.getLogger("wsgi"),
            format="%(REQUEST_METHOD)s - %(REMOTE_ADDR)s - %(status)s - %(HTTP_USER_AGENT)s",
        )
