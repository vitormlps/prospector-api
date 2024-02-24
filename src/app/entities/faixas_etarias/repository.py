#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
# ### Local deps
from ...entities.base.repository import BaseRepo
from .model import FaixaEtaria
from .schema import FaixasEtariasView, FaixasEtariasCreate, FaixasEtariasUpdate


class FaixasEtariasRepo(BaseRepo[FaixaEtaria, FaixasEtariasCreate, FaixasEtariasUpdate]):
    pass


def faixas_etarias_repo():
    return FaixasEtariasRepo(FaixaEtaria)
