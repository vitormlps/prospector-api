#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

# ### Local deps
from ..base.model import Base
from ...utils.type_vars import TypeVars


class CNAEsSecundarios(Base):
    estabelecimento_id: Mapped[UUID] = mapped_column(ForeignKey("estabelecimento.id"), nullable=False, index=True)
    estabelecimento: Mapped[TypeVars.Estabelecimento] = relationship(back_populates="cnaes_secundarios", lazy='subquery')

    cnae_id: Mapped[UUID] = mapped_column(ForeignKey("cnae.id"), nullable=False)
    cnae: Mapped[TypeVars.CNAE] = relationship(lazy='subquery')
