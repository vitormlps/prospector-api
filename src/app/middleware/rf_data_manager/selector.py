#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
import os
import warnings

# ### Third-party deps
import pandas as pd

# ### Local deps
from app.helpers import Logger

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=pd.errors.SettingWithCopyWarning)

class DataSelector:
    def __init__(self) -> None:
        self._logger = Logger().get_logger()
        self._logger.debug("Initializing DataSelector")

        self.cnpj_helper = []
        self.selected_files_path = "./SELECTED_FILES"


    def select_raw_data(self, rf_data, files_path):
        self._logger.debug("Loading raw data")

        for table_name, files_names_list  in rf_data.items():

            if table_name == "estabelecimento" or (
                table_name in [
                    "cnae",
                    "motivo",
                    "natureza_juridica",
                    "qualificacao",
                    "pais",
                    "municipio",
                ]
            ):
                self.cnpj_helper = []
            else:
                if len(self.cnpj_helper) == 0:
                    self.get_cnpjs()

            file_count = 0
            for file_name in files_names_list:
                self._logger.debug(f"Selecting from {file_name}")

                full_file_path = os.path.join(files_path, file_name)

                file_count += 1
                table_reader = pd.read_csv(
                    filepath_or_buffer=full_file_path,
                    sep=";", 
                    skiprows=0,
                    header=None,
                    keep_default_na=False,
                    dtype='object',
                    chunksize=4096,
                    encoding="latin-1",
                    engine="c"
                )

                chunk_count = 0
                for chunk in table_reader:
                    chunk_count += 1
                    filtered_table = self.filter_data_by_specifics(table_name, chunk)

                    if len(filtered_table) > 0:
                        self.save_filtered_table(table_name, filtered_table, chunk_count, file_count)


    def filter_data_by_specifics(self, table_name, table):
        match table_name:
            case "estabelecimento":
                # col 20 is MUNICIPIO, 8801 is PORTO ALEGRE
                table.drop(table.loc[table[20] != "8801"].index, inplace=True)
                # col 5 is SITUACAO_CADASTRAL, 01 is NULA; 04 is INAPTA
                table.drop(table.loc[table[5] == "01"].index, inplace=True)
                table.drop(table.loc[table[5] == "04"].index, inplace=True)
                
                keys = list(table.columns.values)[0]
                indexes = table.set_index(keys).index
                self.cnpj_helper.extend(indexes)

            case "empresa":
                table = self.filter_by_cnpj(table)
                # col 6 is ENTE_FEDERATIVO, not empty means public company
                table.drop(table.loc[table[6] != ""].index, inplace=True)

            case "socio":
                table = self.filter_by_cnpj(table)

            case "simples_nacional":
                table = self.filter_by_cnpj(table)

        return table


    def filter_by_cnpj(self, table):
        keys = list(table.columns.values)[0]
        indexes = table.set_index(keys).index
        return table[indexes.isin(self.cnpj_helper)]


    def save_filtered_table(self, table_name, filtered_table, chunk_count, file_count):
        filtered_table.to_csv(
            path_or_buf=f"{self.selected_files_path}/{table_name}_{file_count}_{chunk_count}.csv",
            sep=";", 
            header=False,
            index=False,
            columns=[i for i in range(filtered_table.shape[1])],
            mode="w", # "a"
            encoding="latin-1",
        )


    def get_cnpjs(self):
        self._logger.debug("Getting selected CNPJs")
        files_paths = []

        with os.scandir(self.selected_files_path) as files:
            for file in files:
                files_paths.append(file.path)

        for path in files_paths:
            if "estabelecimento" in path:
                table = pd.read_csv(
                        filepath_or_buffer=path,
                        sep=";", 
                        skiprows=0,
                        header=None,
                        keep_default_na=False,
                        dtype='object',
                        encoding="latin-1",
                        engine="c" # "pyarrow"
                    )
                keys = list(table.columns.values)[0]
                indexes = table.set_index(keys).index
                self.cnpj_helper.extend(indexes)


    def create_dir(self):
        if not os.path.exists(self.selected_files_path):
            self._logger.debug("Creating folders")
            os.makedirs(self.selected_files_path)


    def start(self, rf_data, files_path):
        self._logger.debug("Starting DataSelector")

        self.create_dir()
        self.select_raw_data(rf_data, files_path)
