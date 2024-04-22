#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
import datetime as dt
import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

# ### Third-party deps
# ### Local deps
from ..utils.singleton import SingletonMeta


# Thread-safe Singleton: https://refactoring.guru/design-patterns/singleton/python/example#example-1
class Logger(metaclass=SingletonMeta):
    """
    A singleton utility class for setting up and configuring a logger with both console and file handlers.

    This class simplifies the process of creating and configuring a logger for logging messages to the console and
    a rotating log file.

    Args:
        logger_name (str, optional): The name of the logger. Defaults to 'auditor'.
        log_dir (str, optional): The directory where log files will be stored. Defaults to 'logs'.
        log_level (str, optional): The log level (e.g., INFO, DEBUG, etc.). Defaults to None.
    """
    _instance = None


    def __init__(self, logger_name = None, log_dir = None, log_level = None):
        """
        Initialize the Logger instance with the specified log name, directory, and log level.

        Args:
            logger_name (str, optional): The name of the logger.
            log_dir (str, optional): The directory where log files will be stored.
            log_level (str, optional): The log level (e.g., INFO, DEBUG, etc.).
        """
        self.logger = logging.getLogger(logger_name)
        self._set_log_level(log_level)

        log_format = self._set_log_formatter()
        self._set_console_handler(self.logger, log_format)

        self._set_log_dir(log_dir)
        self._set_file_handler(self.logger, log_format, log_dir)


    def _set_log_level(self, level: str):
        """
        Set the log level for the logger.

        Args:
            level (str): The log level (e.g., INFO, DEBUG, etc.).
        """
        self.logger.setLevel(level)


    def _set_log_formatter(self):
        return logging.Formatter(
            '[%(asctime)s] %(levelname)s [%(threadName)s | %(module)s.%(funcName)s:%(lineno)d] %(message)s',
            # "%(asctime)s %(levelname)s [%(pathname)s:%(funcName)s:%(lineno)d] %(message)s"
        )


    def _set_console_handler(self, logger, log_format):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(log_format)

        logger.addHandler(console_handler)


    def _set_log_dir(self, log_dir):
        log_dir = Path(log_dir).expanduser().resolve()
        log_dir.mkdir(parents=True, exist_ok=True)


    def _set_file_handler(self, logger, log_format, log_dir: str):
        file_handler = TimedRotatingFileHandler(
            f"{log_dir}/{logger.name}.log", 
            when='midnight', 
            atTime=dt.time(hour=1),
            utc=True,
        )
        file_handler.setFormatter(log_format)

        logger.addHandler(file_handler)


    def get_logger(self):
        """
        Get the singleton logger instance.

        Returns:
            logging.Logger: The singleton logger instance.
        """
        return self.logger
