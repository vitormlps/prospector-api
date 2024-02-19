#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
import os

# ### Third-party deps
import zipfile

# ### Local deps


class DataExtractor:
    def __init__(self) -> None:
        pass

    def extract_files(self, download_path, extraction_path):
        with os.scandir(download_path) as files:
            for file in files:
                if "pdf" not in file.path:
                    with zipfile.ZipFile(file.path, 'r') as zip_ref:
                        zip_ref.extractall(extraction_path)


    def start(self, download_path, extraction_path):
        self.extract_files(download_path, extraction_path)
