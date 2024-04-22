#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
from sqlalchemy.orm import Mapped, mapped_column

# ### Local deps
from ..base.model import Base


class Versionamento(Base):
    rf_last_update: Mapped[str] = mapped_column(unique=True, nullable=False)
