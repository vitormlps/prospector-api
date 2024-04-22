#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
import os
import shutil

# ### Third-party deps
import requests

# ### Local deps
from app.helpers import Logger
from app.entities.versionamentos.repository import versionamentos_repo
from .downloader import DataDownloader
from .extractor import DataExtractor
from .selector import DataSelector
from .populator import DBPopulator


class ReceitaFederalDataManager:
    def __init__(self) -> None:
        self._logger = Logger().get_logger()
        self._logger.debug("Initializing ReceitaFederalDataManager")

        self.rf_data = {
            "cnae": [],
            "motivo": [],
            "natureza_juridica": [],
            "qualificacao": [],
            "pais": [],
            "municipio": [],
            "estabelecimento": [],
            "empresa": [],
            "socio": [],
            "simples_nacional": [],
        }
        self.files_paths = []


    def check_version_diff(self, rf_main_url, update_field_name):
        """
        Verifica a data da última de modificação realizada no repositório da receita federal
        """
        self._logger.info("Checking if there's any update from Receita Federal")

        response = None
        try:
            response = requests.get(rf_main_url)
        except:
            self._logger.info("Couldn't connect to Receita Federal")

        if response:
            rf_updated_date = response.json()[update_field_name]

            repo = versionamentos_repo()
            result = repo.get_all_by(
                {
                    "id": None,
                    "created_at": None,
                    "updated_at": None,
                    "skip": 0,
                    "limit": 0,
                }
            )

            if result and len(result) > 0:
                if result[0].rf_last_update != rf_updated_date:
                    self._logger.info(f"Last update: {result[0].rf_last_update} | RF new update: {rf_updated_date}")
                    return True

        self._logger.info("No updates from Receita Federal")
        return False


    def create_folder(self, path):
        """
        Cria folder caso não exista
        """
        if not os.path.exists(path):
            self._logger.debug("Creating folders")
            os.makedirs(path)


    def files_breakdown(self, extraction_path):
        self._logger.debug("Breaking down files names for database populate")

        items = [name for name in os.listdir(extraction_path) if name.endswith('')]

        for item in items:
            if 'EMPRE' in item:
                self.rf_data["empresa"].append(item)

            elif 'ESTABELE' in item:
                self.rf_data["estabelecimento"].append(item)

            elif 'SOCIO' in item:
                self.rf_data["socio"].append(item)

            elif 'SIMPLES' in item:
                self.rf_data["simples_nacional"].append(item)

            elif 'CNAE' in item:
                self.rf_data["cnae"].append(item)

            elif 'MOTI' in item:
                self.rf_data["motivo"].append(item)

            elif 'MUNIC' in item:
                self.rf_data["municipio"].append(item)

            elif 'NATJU' in item:
                self.rf_data["natureza_juridica"].append(item)

            elif 'PAIS' in item:
                self.rf_data["pais"].append(item)

            elif 'QUALS' in item:
                self.rf_data["qualificacao"].append(item)

            else:
                continue


    def check_files(self, folder_path):
        self._logger.info("Checking for files to delete")

        with os.scandir(folder_path) as files:
            for file in files:
                self.files_paths.append(file.path)


    def delete_files(self):
        self._logger.info("Deleting files")

        for file_path in self.files_paths:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

        self.files_paths.clear()


    def start(self, settings):
        self._logger.debug("Starting ReceitaFederalDataManager")

        is_diff = self.check_version_diff(
            settings.RECEITA_FEDERAL_DATA_MAIN_URL,
            settings.RECEITA_FEDERAL_MAIN_UPDATE_FIELD
        )

        if is_diff:
            self.create_folder(settings.DOWNLOADED_FILES_PATH)

            downloader = DataDownloader(repeat_quantity=10)
            downloader.start(
                settings.RECEITA_FEDERAL_DATA_REPOSITORY_URL,
                settings.RECEITA_FEDERAL_DATA_LAYOUT_URL,
                settings.DOWNLOADED_FILES_PATH,
            )

        if settings.ALLWAYS_EXTRACT:
            self.create_folder(settings.EXTRACTED_FILES_PATH)

            extractor = DataExtractor()
            extractor.start(
                settings.DOWNLOADED_FILES_PATH,
                settings.EXTRACTED_FILES_PATH,
            )
            self.check_files(settings.DOWNLOADED_FILES_PATH)
            if len(self.files_paths) != 0:
                self.delete_files()

        if settings.FILTER_DATA:
            self.files_breakdown(settings.EXTRACTED_FILES_PATH)
            selector = DataSelector()
            selector.start(
                self.rf_data,
                settings.EXTRACTED_FILES_PATH
            )
            self.check_files(settings.EXTRACTED_FILES_PATH)
            if len(self.files_paths) != 0:
                self.delete_files()

        if settings.POPULATE_DB:
            populator = DBPopulator()
            populator.start(settings.RESET_DB)
