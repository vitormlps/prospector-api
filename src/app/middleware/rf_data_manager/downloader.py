#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
import requests

# ### Local deps


class DataDownloader:
    def __init__(self, repeat_quantity: int) -> None:
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
                    self._files_names.remove(file_name)
                    self._files_names.append(f"{file_name}{i}")


    def download_file(self, rf_data_url, download_path, file_name, file_ext):
        response = requests.get(f"{rf_data_url}/{file_name}.{file_ext}")

        if response:
            open(f"{download_path}/{file_name}.{file_ext}", "wb").write(response.content)


    def start(self, rf_data_repo_url, rf_data_layout_url, download_path):
        file_extension = "pdf"
        layout_name = "NOVOLAYOUTDOSDADOSABERTOSDOCNPJ"

        self.download_file(rf_data_layout_url, download_path, layout_name, file_extension)

        file_extension = "zip"
        for file_name in self._files_names:
            self.download_file(rf_data_repo_url, download_path, file_name, file_extension)
