#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
import os

# ### Third-party deps
import requests

# ### Local deps
from .downloader import DataDownloader
from .extractor import DataExtractor


class ReceitaFederalDataManager:
    def __init__(self) -> None:
        self.empresas = []
        self.estabelecimentos = []
        self.socios = []
        self.simples = []
        self.cnaes = []
        self.motivos = []
        self.municipios = []
        self.naturezas_juridicas = []
        self.paises = []
        self.qualificacoes = []


    def check_version_diff(self, rf_main_url, update_field_name):
        """
        Verifica a data da última de modificação realizada no repositório da receita federal
        """
        response = requests.get(rf_main_url)

        if response:
            rf_updated_date = response.json()[update_field_name]

            # Buscar no banco da data da última modificação realizada
            db_updated_date = "18/01/2024 10:34:38" #placeholder

            if db_updated_date != rf_updated_date:
                return True

        return False


    def create_folder(self, path):
        """
        Cria folder caso não exista
        """

        if not os.path.exists(path):
            os.makedirs(path)


    def files_breakdown(self, extraction_path):
        items = [name for name in os.listdir(extraction_path) if name.endswith('')]
        print(items)

        for item in items:
            if 'EMPRE' in item:
                self.empresas.append(item)

            elif 'ESTABELE' in item:
                self.estabelecimentos.append(item)

            elif 'SOCIO' in item:
                self.socios.append(item)

            elif 'SIMPLES' in item:
                self.simples.append(item)

            elif 'CNAE' in item:
                self.cnaes.append(item)

            elif 'MOTI' in item:
                self.motivos.append(item)

            elif 'MUNIC' in item:
                self.municipios.append(item)

            elif 'NATJU' in item:
                self.naturezas_juridicas.append(item)

            elif 'PAIS' in item:
                self.paises.append(item)

            elif 'QUALS' in item:
                self.qualificacoes.append(item)

            else:
                continue


    def start(self, settings):
        is_diff = self.check_version_diff(
            settings.RECEITA_FEDERAL_DATA_MAIN_URL,
            settings.RECEITA_FEDERAL_MAIN_UPDATE_FIELD
        )
        if not is_diff:
            return

        self.create_folder(settings.DOWNLOADED_FILES_PATH)

        downloader = DataDownloader(repeat_quantity=10)
        downloader.start(
            settings.RECEITA_FEDERAL_DATA_REPOSITORY_URL,
            settings.RECEITA_FEDERAL_DATA_LAYOUT_URL,
            settings.DOWNLOADED_FILES_PATH,
        )

        self.create_folder(settings.EXTRACTED_FILES_PATH)

        extractor = DataExtractor()
        extractor.start(
            settings.DOWNLOADED_FILES_PATH,
            settings.EXTRACTED_FILES_PATH,
        )

        self.files_breakdown()

        # insert empresas
        # insert estabelecimentos
        # ...
