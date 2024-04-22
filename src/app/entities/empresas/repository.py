#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
from sqlalchemy import select

# ### Local deps
from ...entities.base.repository import BaseRepo
from .model import Empresa
from .schema import EmpresasView, EmpresasCreate, EmpresasUpdate, EmpresasFilter


class EmpresasRepo(BaseRepo[Empresa, EmpresasCreate, EmpresasUpdate]):
    def get_all_ids(self):
        query = select(self.model.id, self.model.cnpj_basico)
        results = self.session.execute(query).all()
        return results


    def filter_by(
        self,
        filters, 
        order_by: str = "created_at", 
    ):
        
        # fazer filtro com join em estabelecimentos, simples, socios

        query = select(self.model).filter_by(**filters).order_by(order_by)


        results = self.session.execute(query).all()

        return results


def empresas_repo():
    return EmpresasRepo(Empresa)
