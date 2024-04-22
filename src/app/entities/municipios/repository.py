#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
from sqlalchemy import select

# ### Local deps
from ...entities.base.repository import BaseRepo
from .model import Municipio
from .schema import MunicipiosView, MunicipiosCreate, MunicipiosUpdate


class MunicipiosRepo(BaseRepo[Municipio, MunicipiosCreate, MunicipiosUpdate]):
    def get_all_ids(self):
        query = select(self.model.id, self.model.codigo)
        results = self.session.execute(query).all()
        return results


def municipios_repo():
    return MunicipiosRepo(Municipio)
