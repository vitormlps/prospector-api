#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
# ### Local deps
from ...entities.base.repository import BaseRepo
from .model import PorteEmpresa
from .schema import PortesEmpresasView, PortesEmpresasCreate, PortesEmpresasUpdate


class PortesEmpresasRepo(BaseRepo[PorteEmpresa, PortesEmpresasCreate, PortesEmpresasUpdate]):
    pass


def portes_empresas_repo():
    return PortesEmpresasRepo(PorteEmpresa)
