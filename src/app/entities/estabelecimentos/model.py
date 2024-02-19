#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

# ### Local deps
from ..base.model import Base


class Estabelecimentos(Base):
    cnpj_ordem = Column(String(), nullable=False)
    cnpj_digit_verif = Column(String(), nullable=False)
    identificador_matriz_filial = Column(String(), nullable=False)
    nome_fantasia = Column(String(), nullable=False)
    situacao_cadastral = Column(String(), nullable=False)
    data_situacao_cadastral = Column(DateTime, nullable=False)
    motivo_situacao_cadastral = Column(String(), nullable=False)
    nome_cidade_exterior = Column(String(), nullable=False)
    data_inicio_atividade = Column(DateTime, nullable=False)
    tipo_logradouro = Column(String(), nullable=False)
    logradouro = Column(String(), nullable=False)
    numero = Column(String(), nullable=False)
    complemento = Column(String(), nullable=False)
    bairro = Column(String(), nullable=False)
    cep = Column(String(), nullable=False)
    uf = Column(String(), nullable=False)
    ddd_1 = Column(String(), nullable=False)
    telefone_1 = Column(String(), nullable=False)
    ddd_2 = Column(String(), nullable=False)
    telefone_2 = Column(String(), nullable=False)
    ddd_fax = Column(String(), nullable=False)
    fax = Column(String(), nullable=False)
    correio_eletronico = Column(String(), nullable=False)
    situacao_especial = Column(String(), nullable=False)
    data_situacao_especial = Column(DateTime, nullable=False)

    cnpj_basico_id = Column(String(), ForeignKey("empresas.id"))
    cnpj_basico = relationship("Empresas", back_populates="estabelecimentos", lazy="subquery")

    pais_id = Column(String(), ForeignKey("paises.id"))
    pais = relationship("Paises", back_populates="estabelecimentos", lazy="subquery")

    municipio_id = Column(String(), ForeignKey("municipios.id"))
    municipio = relationship("Municipios", back_populates="estabelecimentos", lazy="subquery")

    cnae_fiscal_principal_id = Column(String(), ForeignKey("CNAEs.id"))
    cnae_fiscal_principal = relationship("CNAEs", back_populates="estabelecimentos", lazy="subquery")

    cnae_fiscal_secundaria_id = Column(String(), ForeignKey("CNAEs.id"))
    cnae_fiscal_secundaria = relationship("CNAEs", back_populates="estabelecimentos", lazy="subquery")
