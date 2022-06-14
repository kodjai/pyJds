from logging import Formatter, Logger, handlers, StreamHandler, getLogger, DEBUG
from logging.handlers import TimedRotatingFileHandler
import logging


class Logger:
    _instancs = None

    def __init__(self) -> None:
        self.__logger = getLogger(__name__)
        self.__handler = None

    @classmethod
    def get_instance(cls):
        if cls._instancs is None:
            cls._instancs = cls()

        return cls._instancs

    @classmethod
    def get_logger(cls, level=logging.INFO):
        logger = logging.getLogger()
        # フォーマッターを作成
        formatter = logging.Formatter(
            "%(asctime)s %(name)s %(funcName)s [%(levelname)s]: %(message)s"
        )

        # ハンドラーを作成しフォーマッターを設定
        handler = TimedRotatingFileHandler(
            filename="pyjds.log",
            when="MIDNIGHT",
            interval=1,
            backupCount=31,
        )
        handler.setFormatter(formatter)

        # ロガーにハンドラーを設定、イベント捕捉のためのレベルを設定
        logger.addHandler(handler)
        logger.setLevel(level)

        return logger

    def root_logger(self, file_name: str) -> Logger:
        if self.__handler == None:
            # formatterを作成
            formatter = Formatter(
                "%(asctime)s %(name)s %(funcName)s [%(levelname)s]: %(message)s"
            )

            # ハンドラーを作成しフォーマッターを設定
            self.__handler = TimedRotatingFileHandler(
                filename=file_name,
                when="D",
                interval=1,
                backupCount=31,
            )

            self.__handler.setFormatter(formatter)

            # loggerにhandlerを設定、イベント捕捉のためのレベルを設定
            self.__logger.addHandler(self.__handler)
            # log levelを設定
            self.__logger.setLevel(DEBUG)

        return self.__logger
