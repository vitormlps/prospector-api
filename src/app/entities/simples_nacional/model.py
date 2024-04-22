#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from datetime import datetime

# ### Third-party deps
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
# from sqlalchemy.dialects.postgresql import UUID

# ### Local deps
from ..base.model import Base


class SimplesNacional(Base):
    opcao_simples: Mapped[bool] = mapped_column(nullable=False)
    data_opcao_simples: Mapped[datetime] = mapped_column(nullable=True)
    data_exclusao_simples: Mapped[datetime] = mapped_column(nullable=True)
    opcao_mei: Mapped[bool] = mapped_column(nullable=False)
    data_opcao_mei: Mapped[datetime] = mapped_column(nullable=True)
    data_exclusao_mei: Mapped[datetime] = mapped_column(nullable=True)

    empresa_cnpj: Mapped[str] = mapped_column(ForeignKey("empresa.cnpj_basico"), nullable=False, index=True)
    # empresa = relationship("Empresa", back_populates="simples_nacional", lazy="subquery")
