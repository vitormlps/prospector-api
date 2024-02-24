#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

# ### Local deps
from ..base.model import Base
from ...utils.type_vars import TypeVars


class SimplesNacional(Base):
    opcao_simples: Mapped[bool] = mapped_column(nullable=False)
    data_opcao_simples: Mapped[DateTime] = mapped_column(nullable=True)
    data_exclusao_simples: Mapped[DateTime] = mapped_column(nullable=True)
    opcao_mei: Mapped[bool] = mapped_column(nullable=False)
    data_opcao_mei: Mapped[DateTime] = mapped_column(nullable=True)
    data_exclusao_mei: Mapped[DateTime] = mapped_column(nullable=True)

    empresa_id: Mapped[UUID] = mapped_column(ForeignKey("empresa.id"), nullable=False, index=True)
    empresa: Mapped[TypeVars.Empresa] = relationship(back_populates="simples_nacional", lazy="subquery")
