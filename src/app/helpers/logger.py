#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
import sys
import pathlib as pl
import logging
from logging import handlers

# ### Third-party deps
# ### Local deps


class Logger():
    logger = None

    @staticmethod
    def get_logger():
        return Logger.logger

    @staticmethod
    def setup_logger(app_name: str, env: str):
        Logger.logger = logging.getLogger(app_name)

        if env != "development":
            Logger.logger.setLevel(logging.INFO)
            log_format = Logger.set_info_formatter()

        else:
            Logger.logger.setLevel(logging.DEBUG)
            log_format = Logger.set_debug_formatter()

        Logger.set_console_handler(Logger.logger, log_format)
        
        Logger.set_file_handler(Logger.logger, log_format)


    @staticmethod
    def set_debug_formatter():
        return logging.Formatter(
            "%(asctime)s %(levelname)s [%(module)s.%(funcName)s:%(lineno)d] %(message)s"
        )

    @staticmethod
    def set_info_formatter():
        return logging.Formatter(
            "%(asctime)s %(message)s"
        )


    @staticmethod
    def set_console_handler(logger, log_format):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(log_format)

        logger.addHandler(console_handler)


    @staticmethod
    def set_file_handler(logger, log_format):
        log_dir = pl.Path("logs").expanduser().resolve()
        log_dir.mkdir(parents=True, exist_ok=True)

        file_handler = handlers.TimedRotatingFileHandler(
            log_dir / "auditor.log",
            when="midnight",
            utc=True,
        )

        file_handler.setFormatter(log_format)

        logger.addHandler(file_handler)
