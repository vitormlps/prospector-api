#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
from sqlalchemy import select

# ### Local deps
from ...entities.base.repository import BaseRepo
from .model import PorteEmpresa
from .schema import PortesEmpresasView, PortesEmpresasCreate, PortesEmpresasUpdate


class PortesEmpresasRepo(BaseRepo[PorteEmpresa, PortesEmpresasCreate, PortesEmpresasUpdate]):
    def get_all_ids(self):
        query = select(self.model.id, self.model.codigo)
        results = self.session.execute(query).all()
        return results


def portes_empresas_repo():
    return PortesEmpresasRepo(PorteEmpresa)
