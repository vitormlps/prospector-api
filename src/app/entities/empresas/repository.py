#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
# ### Local deps
from ...entities.base.repository import BaseRepo
from .model import Empresa
from .schema import EmpresasView, EmpresasCreate, EmpresasUpdate


class EmpresasRepo(BaseRepo[Empresa, EmpresasCreate, EmpresasUpdate]):
    pass


def empresas_repo():
    return EmpresasRepo(Empresa)
