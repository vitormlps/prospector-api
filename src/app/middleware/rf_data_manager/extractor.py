#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
import os

# ### Third-party deps
import zipfile

# ### Local deps
from app.helpers import Logger


class DataExtractor:
    def __init__(self) -> None:
        self._logger = Logger().get_logger()
        self._logger.debug("Initializing DataExtractor")


    def extract_files(self, download_path, extraction_path):
        self._logger.info(f"Extracting files from {download_path} to {extraction_path}")

        with os.scandir(download_path) as files:
            for file in files:
                if "pdf" not in file.path:
                    with zipfile.ZipFile(file.path, 'r') as zip_ref:
                        zip_ref.extractall(extraction_path)


    def start(self, download_path, extraction_path):
        self._logger.debug("Starting DataExtractor")
        
        self.extract_files(download_path, extraction_path)
