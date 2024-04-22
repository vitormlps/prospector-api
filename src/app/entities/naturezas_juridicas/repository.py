#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
from sqlalchemy import select

# ### Local deps
from ...entities.base.repository import BaseRepo
from .model import NaturezaJuridica
from .schema import NaturezasJuridicasView, NaturezasJuridicasCreate, NaturezasJuridicasUpdate


class NaturezasJuridicasRepo(BaseRepo[NaturezaJuridica, NaturezasJuridicasCreate, NaturezasJuridicasUpdate]):
    def get_all_ids(self):
        query = select(self.model.id, self.model.codigo)
        results = self.session.execute(query).all()
        return results

def naturezas_juridicas_repo():
    return NaturezasJuridicasRepo(NaturezaJuridica)
