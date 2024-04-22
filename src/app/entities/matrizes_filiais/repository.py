#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
from sqlalchemy import select

# ### Local deps
from ...entities.base.repository import BaseRepo
from .model import MatrizFilial
from .schema import MatrizesFiliaisView, MatrizesFiliaisCreate, MatrizesFiliaisUpdate


class MatrizesFiliaisRepo(BaseRepo[MatrizFilial, MatrizesFiliaisCreate, MatrizesFiliaisUpdate]):
    def get_all_ids(self):
        query = select(self.model.id, self.model.codigo)
        results = self.session.execute(query).all()
        return results


def matrizes_filiais_repo():
    return MatrizesFiliaisRepo(MatrizFilial)
