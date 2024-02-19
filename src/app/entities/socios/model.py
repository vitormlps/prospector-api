#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

# ### Local deps
from ..base.model import Base


class Socios(Base):
    nome = Column(String(), nullable=False, unique=True)
    identificador = Column(String(), nullable=False, unique=True)
    cpf_cnpj = Column(String(), nullable=False)
    qualificacao = Column(String(), nullable=False)
    data_entrada_sociedade = Column(DateTime, nullable=False)
    cpf_representante_legal = Column(String(), nullable=False)
    nome_representante_legal = Column(String(), nullable=False)
    qualificacao_representante_legal = Column(String(), nullable=False)
    faixa_etaria = Column(String(), nullable=False)

    pais_id = Column(String(), ForeignKey("paises.id"))
    pais = relationship("Paises", back_populates="estabelecimentos", lazy="subquery")
