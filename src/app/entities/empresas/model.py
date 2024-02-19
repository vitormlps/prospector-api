#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship

# ### Local deps
from ..base.model import Base


class Empresas(Base):
    cnpj_basico = Column(String(8), nullable=False, unique=True)
    razao_social = Column(String(), nullable=False)
    capital_social = Column(Float, nullable=False)
    porte_empresa = Column(String(2), nullable=False)
    ente_federativo_responsavel = Column(String(), nullable=True)

    natureza_juridica_id = Column(String(), ForeignKey("natureza_juridica.id"))
    natureza_juridica = relationship("NaturezasJuridicas", back_populates="empresas", lazy="subquery")

    qualificacao_responsavel_id = Column(String(), ForeignKey("qualificacao_responsavel.id"))
    qualificacao_responsavel = relationship("Qualificacoes", back_populates="empresas", lazy="subquery")

    estabelecimento = relationship("Estabelecimentos", back_populates="empresas", lazy="subquery")
    socios = relationship("Socios", back_populates="empresas", lazy="subquery")
    simples = relationship("SimplesNacional", back_populates="empresas", lazy="subquery")
