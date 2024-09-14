#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from typing import List, Dict
from uuid import UUID
# from datetime import datetime, timezone, timedelta
from io import BytesIO
import pandas as pd

# ### Third-party deps
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.sql import functions as func

# ### Local deps
from ...entities.base.repository import BaseRepo
from .model import Empresa
from ..qualificacoes.model import Qualificacao
from ..naturezas_juridicas.model import NaturezaJuridica
from ..portes_empresas.model import PorteEmpresa
from ..simples_nacional.model import SimplesNacional
from ..estabelecimentos.model import Estabelecimento
from ..situacoes_cadastrais.model import SituacaoCadastral
from ..cnaes.model import CNAE
from ..motivos.model import Motivo
from ..logradouros.model import Logradouro
from ..municipios.model import Municipio
from .schema import EmpresasView, EmpresasCreate, EmpresasUpdate, EmpresasFilter, EmpresasMainView


class EmpresasRepo(BaseRepo[Empresa, EmpresasCreate, EmpresasUpdate]):
    def get_all_ids(self):
        query = select(self.model.id, self.model.cnpj_basico)
        results = self.session.execute(query).all()
        return results


    def get_all_by(self, filters: BaseModel) -> List[Empresa]:
        filters: Dict = filters.dict()

        query = select(
                self.model.id,
                func.concat(
                    self.model.cnpj_basico,
                    "/",
                    Estabelecimento.cnpj_ordem,
                    "-",
                    Estabelecimento.cnpj_digit_verif
                ).label("cnpj"),
                self.model.razao_social,
                Estabelecimento.nome_fantasia,
                self.model.capital_social,
                NaturezaJuridica.descricao.label("natureza_juridica"),
                CNAE.descricao.label("cnae"),
                Estabelecimento.cnaes_secundarios,
                PorteEmpresa.descricao.label("porte_empresa"),
                SituacaoCadastral.descricao.label("situacao_cadastral"),
                Motivo.descricao.label("motivo"),
                Qualificacao.descricao.label("qualificacao"),
                Logradouro.cep,
                func.concat(
                    Municipio.descricao.label("municipio"),
                    "/",
                    Logradouro.estado_uf.label("uf")
                ).label("municipio"),
                SimplesNacional.opcao_simples,
                SimplesNacional.data_opcao_simples,
                SimplesNacional.data_exclusao_simples
            ).join(Qualificacao
            ).join(NaturezaJuridica
            ).join(PorteEmpresa
            ).join(SimplesNacional
            ).join(Estabelecimento
            ).join(SituacaoCadastral
            ).join(CNAE
            ).join(Motivo
            ).join(Logradouro
            ).join(Municipio
        )

        if filters["natureza_juridica_id"]:
            query = query.where(
                NaturezaJuridica.id.in_(filters["natureza_juridica_id"])
            )

        if filters["porte_empresa_id"]:
            query = query.where(
                PorteEmpresa.id.in_(filters["porte_empresa_id"])
            )

        if filters["situacao_cadastral_id"]:
            query = query.where(
                SituacaoCadastral.id.in_(filters["situacao_cadastral_id"])
            )

        if filters["cnae_id"]:
            query = query.where(
                CNAE.id.in_(filters["cnae_id"])
            )

        if filters["min_capital_social"] != 0 and filters["max_capital_social"] != 0:
            query = query.where(
                self.model.capital_social >= filters["min_capital_social"], 
                self.model.capital_social <= filters["max_capital_social"]
            )

        if filters["opcao_simples"] or filters["opcao_mei"]:
            query = query.where(
                SimplesNacional.opcao_simples == filters["opcao_simples"], 
                SimplesNacional.opcao_mei == filters["opcao_mei"]
            )

        if filters["skip"] != 0:
            query = query.offset(filters["skip"])
        
        if filters["limit"] != 0:
            query = query.limit(filters["limit"])

        results = self.session.execute(query).all()

        return results


    def generate_csv(self, selected_ids: List[UUID]) -> BytesIO | None:
        query = select(
                func.concat(
                    self.model.cnpj_basico,
                    "/",
                    Estabelecimento.cnpj_ordem,
                    "-",
                    Estabelecimento.cnpj_digit_verif
                ).label("cnpj"),
                self.model.razao_social,
                Estabelecimento.nome_fantasia,
                self.model.capital_social,
                NaturezaJuridica.descricao.label("natureza_juridica"),
                CNAE.descricao.label("cnae"),
                Estabelecimento.cnaes_secundarios,
                PorteEmpresa.descricao.label("porte_empresa"),
                SituacaoCadastral.descricao.label("situacao_cadastral"),
                Motivo.descricao.label("motivo"),
                Qualificacao.descricao.label("qualificacao"),
                Logradouro.cep,
                func.concat(
                    Municipio.descricao.label("municipio"),
                    "/",
                    Logradouro.estado_uf.label("uf")
                ).label("municipio"),
                SimplesNacional.opcao_simples,
                SimplesNacional.data_opcao_simples,
                SimplesNacional.data_exclusao_simples
            ).join(Qualificacao
            ).join(NaturezaJuridica
            ).join(PorteEmpresa
            ).join(SimplesNacional
            ).join(Estabelecimento
            ).join(SituacaoCadastral
            ).join(CNAE
            ).join(Motivo
            ).join(Logradouro
            ).join(Municipio
        ).where(
            self.model.id.in_(selected_ids)
        )

        data = self.session.execute(query).all()

        if data:
            df = self.sql_to_dataframe(data)

            buffer = BytesIO()
            with pd.ExcelWriter(buffer) as writer:
                df.to_excel(writer, index=False)

            return BytesIO(buffer.getvalue())

        return None


    def sql_to_dataframe(self, data):
        return pd.DataFrame(
            data,
            # columns=result["data"]
        )

def empresas_repo():
    return EmpresasRepo(Empresa)
