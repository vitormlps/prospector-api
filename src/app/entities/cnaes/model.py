#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from typing import List

# ### Third-party deps
from sqlalchemy.orm import relationship, Mapped, mapped_column

# ### Local deps
from ..base.model import Base
from ...utils.type_vars import TypeVars


class CNAE(Base):
    codigo: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    descricao: Mapped[str] = mapped_column(nullable=False)

    estabelecimentos: Mapped[List[TypeVars.Estabelecimento]] = relationship(back_populates="cnae_fiscal_principal", lazy="subquery")
