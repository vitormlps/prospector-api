#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
from sqlalchemy import select

# ### Local deps
from ...entities.base.repository import BaseRepo
from .model import FaixaEtaria
from .schema import FaixasEtariasView, FaixasEtariasCreate, FaixasEtariasUpdate


class FaixasEtariasRepo(BaseRepo[FaixaEtaria, FaixasEtariasCreate, FaixasEtariasUpdate]):
    def get_all_ids(self):
        query = select(self.model.id, self.model.codigo)
        results = self.session.execute(query).all()
        return results


def faixas_etarias_repo():
    return FaixasEtariasRepo(FaixaEtaria)
