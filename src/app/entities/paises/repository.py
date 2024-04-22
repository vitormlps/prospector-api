#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
from sqlalchemy import select

# ### Local deps
from ...entities.base.repository import BaseRepo
from .model import Pais
from .schema import PaisesView, PaisesCreate, PaisesUpdate


class PaisesRepo(BaseRepo[Pais, PaisesCreate, PaisesUpdate]):
    def get_all_ids(self):
        query = select(self.model.id, self.model.codigo)
        results = self.session.execute(query).all()
        return results


def paises_repo():
    return PaisesRepo(Pais)
