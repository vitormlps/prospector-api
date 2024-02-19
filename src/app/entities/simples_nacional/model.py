#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

# ### Local deps
from ..base.model import Base


class SimplesNacional(Base):
    opcao_pelo_simples = Column(String(), nullable=False)
    data_opcao_simples = Column(DateTime, nullable=False)
    data_exclusao_simples = Column(DateTime, nullable=False)
    opcao_mei = Column(String(), nullable=True)
    data_opcao_mei = Column(DateTime, nullable=False)
    data_exclusao_mei = Column(DateTime, nullable=False)

    cnpj_basico_id = Column(String(), ForeignKey("empresas.id"))
    cnpj_basico = relationship("Empresas", back_populates="estabelecimentos", lazy="subquery")
