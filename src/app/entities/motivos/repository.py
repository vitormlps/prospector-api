#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
from sqlalchemy import select

# ### Local deps
from ...entities.base.repository import BaseRepo
from .model import Motivo
from .schema import MotivosView, MotivosCreate, MotivosUpdate


class MotivosRepo(BaseRepo[Motivo, MotivosCreate, MotivosUpdate]):
    def get_all_ids(self):
        query = select(self.model.id, self.model.codigo)
        results = self.session.execute(query).all()
        return results


def motivos_repo():
    return MotivosRepo(Motivo)
