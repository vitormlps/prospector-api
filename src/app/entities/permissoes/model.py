#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from typing import List

# ### Third-party deps
from sqlalchemy.orm import relationship, Mapped, mapped_column

# ### Local deps
from ..base.model import Base
from ...utils.type_vars import TypeVars


class Permissoes(Base):
    tipo: Mapped[str] = mapped_column(nullable=False, insert_default="standard")
    can_view: Mapped[bool] = mapped_column(nullable=False, insert_default=True)
    can_update: Mapped[bool] = mapped_column(nullable=False, insert_default=True)
    can_delete: Mapped[bool] = mapped_column(nullable=False, insert_default=False)

    usuarios: Mapped[List[TypeVars.Usuario]] = relationship(back_populates="permissao", lazy="subquery")
