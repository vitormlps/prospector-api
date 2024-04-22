#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
import os
from datetime import datetime
from uuid import uuid4

# ### Third-party deps
import pandas as pd
from sqlalchemy import String, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID

# ### Local deps
from app.helpers import Logger
from app.database.connection import get_db_local_session, get_db_engine
from app.entities.base.repository import reset_db
from app.entities.versionamentos.repository import versionamentos_repo
from app.entities.cnaes.repository import cnaes_repo
from app.entities.motivos.repository import motivos_repo
from app.entities.municipios.repository import municipios_repo
from app.entities.paises.repository import paises_repo
from app.entities.naturezas_juridicas.repository import naturezas_juridicas_repo
from app.entities.qualificacoes.repository import qualificacoes_repo
from app.entities.matrizes_filiais.repository import matrizes_filiais_repo
from app.entities.portes_empresas.repository import portes_empresas_repo
from app.entities.faixas_etarias.repository import faixas_etarias_repo
from app.entities.representantes_legais.repository import representantes_legais_repo
from app.entities.situacoes_cadastrais.repository import situacoes_cadastrais_repo
from app.entities.logradouros.repository import logradouros_repo
from app.entities.empresas.repository import empresas_repo
from app.entities.estabelecimentos.repository import estabelecimentos_repo
from app.entities.socios.repository import socios_repo
from app.entities.simples_nacional.repository import simples_nacional_repo


class DBPopulator:
    def __init__(self) -> None:
        self._logger = Logger().get_logger()
        self._logger.debug("Initializing DBPopulate")

        self.table_names = [
            "cnae",
            "motivo",
            "natureza_juridica",
            "qualificacao",
            "pais",
            "municipio",
            "empresa",
            "estabelecimento",
            "socio",
            "simples_nacional",
        ]
        self.cnaes = []
        self.motivos = []
        self.municipios = []
        self.paises = []
        self.naturezas_juridicas = []
        self.qualificacoes = []
        self.matrizes_filiais = []
        self.portes_empresas = []
        self.representantes_legais = []
        self.faixas_etarias = []
        self.situacoes_cadastrais = []
        self.empresas = []
        # self.estabelecimentos = []
        # self.socios = []
        # self.simples_nacional = []

        # Faltarão por enquanto
        #  - insert usuarios
        #  - insert permissoes
        
        self.temp_cnpjs = []
        self.temp_logradouros = []
        self.temp_contatos = []
        self.temp_representantes = []

        self.selected_files_path = "./SELECTED_FILES"
        self._default_filters = {
                "id": None,
                "created_at": None,
                "updated_at": None,
                "skip": 0,
                "limit": 0,
            }
        self.table_chunk_size = 4096


    @property
    def default_filters(self):
        return self._default_filters.copy()


    def start(self, reset_db=False):
        self._logger.debug("Starting DBPopulate")

        if reset_db:
            self._reset_database()

        self._populate_extra_tables()
        files_paths = self.get_files_paths()

        self.municipios = municipios_repo().get_all_ids()
        if self.municipios is None:
            self.municipios = []

        self.empresas = empresas_repo().get_all_ids()
        if self.empresas is None:
            self.empresas = []

        if len(self.temp_cnpjs) != len(self.empresas):
            self.temp_cnpjs = [row[1] for row in self.empresas]
        
        self._logger.debug(f"Qtde empresas: {len(self.empresas)}")

        for table_name in self.table_names:
            self._logger.debug(f"Inserting {table_name}")

            if table_name == "empresa" and len(self.empresas) > 0:
                continue

            if table_name == "estabelecimento":
                if estabelecimentos_repo().count() > 0:
                    continue

                if len(self.municipios) == 0:
                    self.municipios = municipios_repo().get_all_ids()

                if len(self.empresas) == 0:
                    self.empresas = empresas_repo().get_all_ids()

            if table_name == "socio" and socios_repo().count() > 0:
                continue

            if table_name == "simples_nacional" and simples_nacional_repo().count() > 0:
                continue

            for index in range(len(files_paths)):
                if table_name in files_paths[index]:
                    table_reader = pd.read_csv(
                            filepath_or_buffer=files_paths[index],
                            sep=";", 
                            skiprows=0,
                            header=None,
                            keep_default_na=False,
                            dtype='object',
                            chunksize=4096,
                            encoding="latin-1",
                            engine="c"
                        )

                    for chunk in table_reader:
                        chunk.insert(0, "id", uuid4())

                        insert_method = self.__getattribute__(f"_insert_{table_name}")
                        insert_method(table_name, chunk)

        self._close_session()


    def get_files_paths(self):
        self._logger.debug("Getting files paths")
        files_paths = []
        with os.scandir(self.selected_files_path) as files:
            files_paths = [file.path for file in files]
        return files_paths


    def to_sql(self, table_name, table, connection, dtypes):
        table.to_sql(
            con=connection,
            name=table_name,
            dtype=dtypes, 
            index=False,
            if_exists="append",
            method="multi",
            chunksize=self.table_chunk_size,
        )


    def _update(self):
        # se linha no csv existe na tabela, verifica se valores estão iguais, se não atualiza.
        # caso linha no csv não exista na tabela e é de um arquivo novo, inserir na tabela
        pass


    def _finalize(self):
        # se count de linhas na tabela for igual ao count de linhas do csv, excluir arquivo
        pass


    def _populate_extra_tables(self):
        extra_tables = [
            "matrizes_filiais", 
            "situacoes_cadastrais",
            "portes_empresas",
            "faixas_etarias",
        ]
        for table_name in extra_tables:
            insert_method = self.__getattribute__(f"_insert_{table_name}")
            insert_method()


    def _get_versao_rf(self):
        repo = versionamentos_repo()

        result = repo.get_all_by(self.default_filters)

        if result and len(result) > 0:
            repo.session.refresh(result[0])
            return result[0].rf_last_update


    def _insert_versao_rf(self, result):
        repo = versionamentos_repo()

        if result:
            result = repo.create({"rf_last_update": result})
        else:
            result = repo.create({"rf_last_update":"20/03/2024 09:51:33"})
        
        repo.session.refresh(result)


    def _reset_database(self):
        self._logger.debug("Reseting database")

        result = self._get_versao_rf()
        reset_db()
        self._insert_versao_rf(result)


    def _close_session(self):
        self._logger.debug("Closing session")
        
        session = get_db_local_session()
        session.close()


    def filter_by_cnpj(self, table):
        keys = list(table.columns.values)[1]
        indexes = table.set_index(keys).index
        return table[indexes.isin(self.temp_cnpjs)]


    def _insert_matrizes_filiais(self):
        self._logger.debug("Inserting matrizes filiais")

        table = [
            ["01", "Matriz"],
            ["02", "Filial"],
        ]
        repo = matrizes_filiais_repo()

        count = repo.count()
        if count == len(table):
            self.matrizes_filiais = repo.get_all_ids()
            return

        for row in table:
            repo.create(
                {
                    "codigo":row[0],
                    "descricao":row[1],
                },
                commit=False
            )
        repo.session.commit()
        self.matrizes_filiais = repo.get_all_ids()


    def _insert_situacoes_cadastrais(self):
        self._logger.debug("Inserting situacoes cadastrais")

        table = [
            ["01", "Nula"],
            ["02", "Ativa"],
            ["03", "Suspensa"],
            ["04", "Inapta"],
            ["05", "-"],
            ["06", "-"],
            ["07", "-"],
            ["08", "Baixada"],
        ]
        repo = situacoes_cadastrais_repo()

        count = repo.count()
        if count == len(table):
            self.situacoes_cadastrais = repo.get_all_ids()
            return

        for row in table:
            repo.create(
                {
                    "codigo":row[0],
                    "descricao":row[1],
                },
                commit=False
            )
        repo.session.commit()
        self.situacoes_cadastrais = repo.get_all_ids()


    def _insert_portes_empresas(self):
        self._logger.debug("Inserting portes empresas")

        table = [
            ["01", "Não informado"],
            ["02", "Micro Empresa"],
            ["03", "Empresa de Pequeno Porte"],
            ["04", "-"],
            ["05", "Demais"],
        ]
        repo = portes_empresas_repo()

        count = repo.count()
        if count == len(table):
            self.portes_empresas = repo.get_all_ids()
            return

        for row in table:
            repo.create(
                {
                    "codigo":row[0],
                    "descricao":row[1],
                },
                commit=False
            )
        repo.session.commit()
        self.portes_empresas = repo.get_all_ids()


    def _insert_faixas_etarias(self):
        self._logger.debug("Inserting Faixas etárias")

        table = [
            ["01", "0 a 12"],
            ["02", "13 a 20"],
            ["03", "21 a 30"],
            ["04", "31 a 40"],
            ["05", "41 a 50"],
            ["06", "51 a 60"],
            ["07", "61 a 70"],
            ["08", "71 a 80"],
            ["09", "81+"],
        ]
        repo = faixas_etarias_repo()

        count = repo.count()
        if count == len(table):
            self.faixas_etarias = repo.get_all_ids()
            return

        for row in table:
            repo.create(
                {
                    "codigo":row[0],
                    "descricao":row[1],
                },
                commit=False
            )
        repo.session.commit()
        self.faixas_etarias = repo.get_all_ids()


    def get_base_columns(self, row):
        now = datetime.now()
        row.loc["id"] = uuid4()

        row.loc["created_at"] = now
        row.loc["updated_at"] = now

        return row


    def get_structure_with_descricao(self, table: pd.DataFrame):
        table = table.rename(columns={
            0: "codigo", 
            1: "descricao",
            2: "created_at",
            3: "updated_at"
        })
        table = table.apply(func=self.get_base_columns, axis=1)
        dtypes = {
            "id": UUID,
            "codigo": String,
            "descricao": String,
            "created_at": DateTime,
            "updated_at": DateTime,
        }
        return table, dtypes


    def _insert_cnae(self, table_name, table: pd.DataFrame):
        repo = cnaes_repo()
        count = repo.count()
        if count == len(table):
            self.cnaes = repo.get_all_ids()
            return
        
        table, dtypes = self.get_structure_with_descricao(table)

        self.to_sql(table_name, table, get_db_engine(), dtypes)
        self.cnaes = repo.get_all_ids()


    def _insert_motivo(self, table_name, table: pd.DataFrame):
        repo = motivos_repo()
        count = repo.count()
        if count == len(table):
            self.motivos = repo.get_all_ids()
            return

        table, dtypes = self.get_structure_with_descricao(table)

        self.to_sql(table_name, table, get_db_engine(), dtypes)
        self.motivos = repo.get_all_ids()


    def _insert_natureza_juridica(self, table_name, table: pd.DataFrame):
        repo = naturezas_juridicas_repo()
        count = repo.count()
        if count == len(table):
            self.naturezas_juridicas = repo.get_all_ids()
            return

        table, dtypes = self.get_structure_with_descricao(table)

        self.to_sql(table_name, table, get_db_engine(), dtypes)
        self.naturezas_juridicas = repo.get_all_ids()


    def _insert_qualificacao(self, table_name, table: pd.DataFrame):
        repo = qualificacoes_repo()
        count = repo.count()
        if count == len(table):
            self.qualificacoes = repo.get_all_ids()
            return

        table, dtypes = self.get_structure_with_descricao(table)

        self.to_sql(table_name, table, get_db_engine(), dtypes)
        self.qualificacoes = repo.get_all_ids()


    def _insert_municipio(self, table_name, table: pd.DataFrame):
        repo = municipios_repo()
        count = repo.count()
        if count == 5571:
            return

        table, dtypes = self.get_structure_with_descricao(table)

        self.to_sql(table_name, table, get_db_engine(), dtypes)


    def _insert_pais(self, table_name, table: pd.DataFrame):
        repo = paises_repo()
        count = repo.count()
        if count == len(table):
            self.paises = repo.get_all_ids()
            return

        table, dtypes = self.get_structure_with_descricao(table)

        self.to_sql(table_name, table, get_db_engine(), dtypes)
        self.paises = repo.get_all_ids()


    def get_empresa_columns(self, row):
        row.loc["capital_social"] = float(row.loc["capital_social"].split(",")[0])

        for i in range(len(self.naturezas_juridicas)):
            if self.naturezas_juridicas[i][1] == str(row.loc["natureza_juridica_id"]):
                row.loc["natureza_juridica_id"] = self.naturezas_juridicas[i][0]
                break

        for i in range(len(self.qualificacoes)):
            if str(row.loc["qualificacao_responsavel_id"]) == "36":
                row.loc["qualificacao_responsavel_id"] = "16"
            if self.qualificacoes[i][1] == str(row.loc["qualificacao_responsavel_id"]):
                row.loc["qualificacao_responsavel_id"] = self.qualificacoes[i][0]
                break

        for i in range(len(self.portes_empresas)):
            if self.portes_empresas[i][1] == str(row.loc["porte_empresa_id"]):
                row.loc["porte_empresa_id"] = self.portes_empresas[i][0]
                break

        row = self.get_base_columns(row)
        self.temp_cnpjs.append(row.loc["cnpj_basico"])
        return row


    def _insert_empresa(self, table_name, table: pd.DataFrame):
        table = table.rename(columns={
            0: "cnpj_basico", 
            1: "razao_social",
            2: "natureza_juridica_id",
            3: "qualificacao_responsavel_id",
            4: "capital_social",
            5: "porte_empresa_id",
            6: "created_at",
            7: "updated_at"
        })

        table = table[~table.cnpj_basico.isin(self.temp_cnpjs)]
        table = table.apply(func=self.get_empresa_columns, axis=1)

        dtypes = {
            "id": UUID,
            "cnpj_basico": String,
            "razao_social": String,
            "natureza_juridica_id": UUID,
            "qualificacao_responsavel_id": UUID,
            "capital_social": Float,
            "porte_empresa_id": UUID,
            "created_at": DateTime,
            "updated_at": DateTime,
        }

        self.to_sql(table_name, table, get_db_engine(), dtypes)


    def get_estabelecimento_columns(self, row):
        now = datetime.now()

        estabelecimento_id = uuid4()
        row.loc["id"] = estabelecimento_id

        for i in range(len(self.matrizes_filiais)):
            if self.matrizes_filiais[i][1] == "0" + str(row.loc["matriz_filial_id"]).strip():
                row.loc["matriz_filial_id"] = self.matrizes_filiais[i][0]
                break
        for i in range(len(self.situacoes_cadastrais)):
            if self.situacoes_cadastrais[i][1] == str(row.loc["situacao_cadastral_id"]).strip():
                row.loc["situacao_cadastral_id"] = self.situacoes_cadastrais[i][0]
                break
        for i in range(len(self.motivos)):
            if self.motivos[i][1] == str(row.loc["motivo_id"]).strip():
                row.loc["motivo_id"] = self.motivos[i][0]
                break

        if row.loc["pais_id"] == '':
            row.loc["pais_id"] = None
        else:
            for i in range(len(self.paises)):
                if self.paises[i][1] == str(row.loc["pais_id"]).strip():
                    row.loc["pais_id"] = self.paises[i][0]
                    break

        for i in range(len(self.cnaes)):
            if self.cnaes[i][1] == str(row.loc["cnae_principal_id"]).strip():
                row.loc["cnae_principal_id"] = self.cnaes[i][0]
                break

        temp = None
        for i in range(len(self.municipios)):
            if self.municipios[i][1] == str(row.loc["municipio"]).strip():
                temp = self.municipios[i][0]
                break

        logradouro_id = uuid4()
        self.temp_logradouros.append({
            "id": logradouro_id,
            "tipo": row.loc["tipo_logradouro"],
            "nome": row.loc["logradouro_id"],
            "numero": row.loc["numero"],
            "complemento": row.loc["complemento"],
            "bairro": row.loc["bairro"],
            "cep": row.loc["cep"],
            "estado_uf": row.loc["estado_uf"],
            "municipio_id": temp,
            "created_at" : now,
            "updated_at" : now,
        })
        row.loc["logradouro_id"] = logradouro_id

        ddd = row.loc['ddd_1']
        fone = row.loc['telefone_1']
        if fone:
            self.temp_contatos.append({
                    "id": uuid4(),
                    "tipo": "Celular" if fone[0] == "9" else "Telefone",
                    "descricao": f"({ddd}){fone}",
                    "estabelecimento_id": estabelecimento_id,
                    "created_at" : now,
                    "updated_at" : now,
                })

        ddd = row.loc['ddd_2']
        fone = row.loc['telefone_2']
        if fone:
            self.temp_contatos.append({
                    "id": uuid4(),
                    "tipo": "Celular" if fone[0] == "9" else "Telefone",
                    "descricao": f"({ddd}){fone}",
                    "estabelecimento_id": estabelecimento_id,
                    "created_at" : now,
                    "updated_at" : now,
                })

        email = row.loc['email']
        if email:
            self.temp_contatos.append({
                "id": uuid4(),
                "tipo": "E-mail",
                "descricao": email,
                "estabelecimento_id": estabelecimento_id,
                "created_at" : now,
                "updated_at" : now,
            })

        temp = row.loc["data_situacao_cadastral"]
        row.loc["data_situacao_cadastral"] = temp if len(temp) >= 8 else '19700101'

        temp = row.loc["data_inicio_atividade"]
        row.loc["data_inicio_atividade"] = temp if len(temp) >= 8 else '19700101'

        temp = row.loc["data_situacao_especial"]
        row.loc["data_situacao_especial"] = temp if len(temp) >= 8 else None

        row.loc["created_at"] = now
        row.loc["updated_at"] = now

        return row


    def _insert_estabelecimento(self, table_name, table: pd.DataFrame):
        table = self.filter_by_cnpj(table)

        table = table.rename(columns={
            0: "empresa_cnpj", 
            1: "cnpj_ordem",
            2: "cnpj_digit_verif",
            3: "matriz_filial_id",
            4: "nome_fantasia",
            5: "situacao_cadastral_id",
            6: "data_situacao_cadastral",
            7: "motivo_id",
            8: "nome_cidade_exterior",
            9: "pais_id",
            10: "data_inicio_atividade",
            11: "cnae_principal_id",
            12: "cnaes_secundarios",
            13: "tipo_logradouro",
            14: "logradouro_id",
            15: "numero",
            16: "complemento",
            17: "bairro",
            18: "cep",
            19: "estado_uf",
            20: "municipio",
            21: "ddd_1",
            22: "telefone_1",
            23: "ddd_2",
            24: "telefone_2",
            25: "ddd_fax",
            26: "fax",
            27: "email",
            28: "situacao_especial",
            29: "data_situacao_especial",
            30: "created_at",
            31: "updated_at"
        })
        table = table.apply(func=self.get_estabelecimento_columns, axis=1)
        table.drop([
            "tipo_logradouro",
            "numero",
            "complemento",
            "bairro",
            "cep",
            "estado_uf",
            "municipio",
            "ddd_1",
            "telefone_1",
            "ddd_2",
            "telefone_2",
            "ddd_fax",
            "fax",
            "email",
        ], axis=1, inplace=True)
        dtypes = {
            "id": UUID,
            "cnpj_ordem": String,
            "cnpj_digit_verif": String,
            "nome_fantasia": String,
            "data_situacao_cadastral": DateTime,
            "nome_cidade_exterior": String,
            "data_inicio_atividade": DateTime,
            "cnaes_secundarios": String,
            "situacao_especial": String,
            "data_situacao_especial": DateTime,
            "empresa_cnpj": String,
            "matriz_filial_id": UUID,
            "situacao_cadastral_id": UUID,
            "motivo_id": UUID,
            "pais_id": UUID,
            "cnae_principal_id": UUID,
            "logradouro_id": UUID,
            "created_at": DateTime,
            "updated_at": DateTime,
        }

        if len(table) > 0:
            self._insert_logradouro(self.temp_logradouros)

        self.to_sql(table_name, table, get_db_engine(), dtypes)

        if len(table) > 0:
            self._insert_contato(self.temp_contatos)


    def _insert_logradouro(self, temp_tables):
        table = pd.DataFrame.from_dict(temp_tables, orient="columns")
        dtypes = {
            "id": UUID,
            "tipo": String,
            "nome": String,
            "numero": String,
            "complemento": String,
            "bairro": String,
            "cep": String,
            "estado_uf": String,
            "municipio_id": UUID,
            "created_at": DateTime,
            "updated_at": DateTime,
        }
        self.to_sql("logradouro", table, get_db_engine(), dtypes)
        temp_tables.clear()


    def _insert_contato(self, temp_tables):
        table = pd.DataFrame.from_dict(temp_tables, orient="columns")
        dtypes = {
            "id": UUID,
            "tipo": String,
            "descricao": String,
            "estabelecimento_id": UUID,
            "created_at": DateTime,
            "updated_at": DateTime,
        }
        self.to_sql("contato", table, get_db_engine(), dtypes)
        temp_tables.clear()


    def get_socio_columns(self, row):
        now = datetime.now()

        socio_id = uuid4()
        row.loc["id"] = socio_id

        for i in range(len(self.qualificacoes)):
            if self.qualificacoes[i][1] == str(row.loc["qualificacao_representante"]).strip():
                row.loc["qualificacao_representante"] = self.qualificacoes[i][0]

            if self.qualificacoes[i][1] == str(row.loc["qualificacao_id"]).strip():
                row.loc["qualificacao_id"] = self.qualificacoes[i][0]

        temp = row.loc["data_entrada_sociedade"]
        row.loc["data_entrada_sociedade"] = temp if len(temp) >= 8 else '19700101'

        if row.loc["pais_id"] == '':
            row.loc["pais_id"] = None
        else:
            for i in range(len(self.paises)):
                if self.paises[i][1] == str(row.loc["pais_id"]).strip():
                    row.loc["pais_id"] = self.paises[i][0]
                    break

        representante = str(row.loc["representante_legal_id"]).strip()
        if representante == "***000000**":
            row.loc["representante_legal_id"] = None
        else:
            representante_id = uuid4()
            self.temp_representantes.append({
                "id": representante_id,
                "cpf": representante,
                "nome": row.loc["nome_representante"],
                "qualificacao_id": row.loc["qualificacao_representante"],
                "created_at" : now,
                "updated_at" : now,
            })
            row.loc["representante_legal_id"] = representante_id

        faixa_etaria = str(row.loc["faixa_etaria_id"]).strip()
        if faixa_etaria == "0":
            row.loc["faixa_etaria_id"] = None
        else:
            for i in range(len(self.faixas_etarias)):
                if self.faixas_etarias[i][1] == "0" + faixa_etaria:
                    row.loc["faixa_etaria_id"] = self.faixas_etarias[i][0]
                    break

        row.loc["created_at"] = now
        row.loc["updated_at"] = now

        return row


    def _insert_socio(self, table_name, table: pd.DataFrame):
        table = self.filter_by_cnpj(table)

        table = table.rename(columns={
            0: "empresa_cnpj", 
            1: "identificador_socio", 
            2: "nome", 
            3: "cpf_cnpj",
            4: "qualificacao_id",
            5: "data_entrada_sociedade",
            6: "pais_id",
            7: "representante_legal_id",
            8: "nome_representante",
            9: "qualificacao_representante",
            10: "faixa_etaria_id",
            11: "created_at",
            12: "updated_at"
        })
        table = table.apply(func=self.get_socio_columns, axis=1)
        table.drop([
            "identificador_socio",
            "nome_representante",
            "qualificacao_representante",
        ], axis=1, inplace=True)
        dtypes = {
            "id": UUID,
            "empresa_cnpj": String,
            "nome": String,
            "cpf_cnpj": String,
            "qualificacao_id": UUID,
            "data_entrada_sociedade": DateTime,
            "pais_id": UUID,
            "representante_legal_id": UUID,
            "faixa_etaria_id": UUID,
            "created_at": DateTime,
            "updated_at": DateTime,
        }

        if len(table) > 0:
            self._insert_representantes_legais(self.temp_representantes)

        self.to_sql(table_name, table, get_db_engine(), dtypes)


    def _insert_representantes_legais(self, temp_tables):
        table = pd.DataFrame.from_dict(temp_tables, orient="columns")
        dtypes = {
            "id": UUID,
            "cpf": String,
            "nome": String,
            "qualificacao_id": UUID,
            "created_at": DateTime,
            "updated_at": DateTime,
        }
        self.to_sql("representante_legal", table, get_db_engine(), dtypes)
        temp_tables.clear()


    def get_simples_columns(self, row):
        if str(row.loc["opcao_simples"]).strip() != "S":
            row.loc["opcao_simples"] = False
        else:
            row.loc["opcao_simples"] = True

        temp = "00000000"
        if temp in str(row.loc["data_opcao_simples"]).strip():
            row.loc["data_opcao_simples"] = None

        if temp in str(row.loc["data_exclusao_simples"]).strip():
            row.loc["data_exclusao_simples"] = None

        if str(row.loc["opcao_mei"]).strip() != "S":
            row.loc["opcao_mei"] = False
        else:
            row.loc["opcao_mei"] = True

        if temp in str(row.loc["data_opcao_mei"]).strip():
            row.loc["data_opcao_mei"] = None

        if temp in str(row.loc["data_exclusao_mei"]).strip():
            row.loc["data_exclusao_mei"] = None

        row = self.get_base_columns(row)
        return row


    def _insert_simples_nacional(self, table_name, table: pd.DataFrame):
        table = self.filter_by_cnpj(table)

        table = table.rename(columns={
            0: "empresa_cnpj",
            1: "opcao_simples",
            2: "data_opcao_simples",
            3: "data_exclusao_simples",
            4: "opcao_mei",
            5: "data_opcao_mei",
            6: "data_exclusao_mei",
            7: "created_at",
            8: "updated_at"
        })
        table = table.apply(func=self.get_simples_columns, axis=1)
        dtypes = {
            "id": UUID,
            "empresa_cnpj": String,
            "opcao_simples": String,
            "data_opcao_simples": DateTime,
            "data_exclusao_simples": DateTime,
            "opcao_mei": String,
            "data_opcao_mei": DateTime,
            "data_exclusao_mei": DateTime,
            "created_at": DateTime,
            "updated_at": DateTime,
        }

        self.to_sql(table_name, table, get_db_engine(), dtypes)
