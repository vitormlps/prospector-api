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


class RepresentanteLegal(Base):
    cpf: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    nome: Mapped[str] = mapped_column(nullable=False)

    qualificacao_id: Mapped[UUID] = mapped_column(ForeignKey("qualificacao.id"), nullable=False)
    qualificacao: Mapped[TypeVars.Qualificacao] = relationship(lazy="subquery")
