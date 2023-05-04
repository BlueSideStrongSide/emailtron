import logging
import pathlib
from pathlib import Path
from abc import ABC

class HgMessageLogger:

    def __init__(self, logging_options):

        self.logger = logging.getLogger(self.__class__.__name__)

        self._logging_level = logging_options.get("level", "INFO").upper()
        self._stream_handler = None
        self._file_handler = None
        self._formatter = None

        self.configure_logging(logging_options)

    def configure_logging(self,logging_options):

        self.logging_level()
        self.logging_stream_handler()
        self.logging_file_handler()
        self.logging_formatter()

    def logging_level(self):

        supported_level = ["DEBUG","INFO","WARNING","ERROR","CRITICAL"]

        if self._logging_level in supported_level:
            self.logger.setLevel(self._logging_level)

    def logging_stream_handler(self):
        self._stream_handler = logging.StreamHandler()
        self._stream_handler.setLevel(self._logging_level)

    def logging_file_handler(self):
        #these will static for now, stream and file logging only
        #update call to use a variable and splite off file extension
        if not pathlib.Path("logs/").is_file():
            pathlib.Path("logs/").mkdir(parents=True, exist_ok=True)

        self._file_handler = logging.FileHandler(filename="logs/dev_log.log", mode="a")
        self._file_handler.setLevel(self._logging_level)

    def logging_formatter(self):
        # static for now one format for all modules
        self._formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        self._file_handler.setFormatter(self._formatter)
        self._stream_handler.setFormatter(self._formatter)

        self.logger.addHandler(self._file_handler)
        self.logger.addHandler(self._stream_handler)


if __name__ == '__main__':
    message_local_test = HgMessageLogger()
    message_local_test.logger("This is a test message")