#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
import os

# ### Third-party deps
import requests

# ### Local deps
from app.helpers import Logger


class DataDownloader:
    def __init__(self, repeat_quantity: int) -> None:
        self._logger = Logger().get_logger()
        self._logger.debug("Initializing DataDownloader")

        self._files_names = [
            "Cnaes",
            "Motivos",
            "Municipios",
            "Naturezas",
            "Paises",
            "Qualificacoes",
            "Simples",
            "Socios",
            "Empresas",
            "Estabelecimentos",
        ]
        temp_names = self._files_names

        for file_name in temp_names:
            if file_name in ["Socios", "Empresas", "Estabelecimentos"]:

                for i in range(repeat_quantity):
                    self._files_names.append(f"{file_name}{i}")
        
        self._files_names.remove("Socios")
        self._files_names.remove("Empresas")
        self._files_names.remove("Estabelecimentos")


    def check_file_exists(self, download_path, file_name, file_ext):
        if os.path.exists(f"{download_path}/{file_name}.{file_ext}"):
            return True
        
        return False


    def download_file(self, rf_data_url, download_path, file_name, file_ext):
        self._logger.info(f"Downloading file {file_name}")

        response = requests.get(f"{rf_data_url}/{file_name}.{file_ext}")

        if response:
            open(f"{download_path}/{file_name}.{file_ext}", "wb").write(response.content)


    def start(self, rf_data_repo_url, rf_data_layout_url, download_path):
        self._logger.debug("Starting DataDownloader")

        file_extension = "pdf"
        layout_name = "NOVOLAYOUTDOSDADOSABERTOSDOCNPJ"

        self.download_file(rf_data_layout_url, download_path, layout_name, file_extension)

        file_extension = "zip"
        for file_name in self._files_names:
            exists = self.check_file_exists(download_path, file_name, file_extension)
            
            if not exists:
                self.download_file(rf_data_repo_url, download_path, file_name, file_extension)
