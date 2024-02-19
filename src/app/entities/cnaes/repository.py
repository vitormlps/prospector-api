#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
# ### Local deps
from ...entities.base.repository import BaseRepo
from .model import CNAEs
from .schema import CNAEsView, CNAEsCreate, CNAEsUpdate


class CNAEsRepo(BaseRepo[CNAEs, CNAEsCreate, CNAEsUpdate]):
    pass

    # @staticmethod
    # def get_index_sequence(session):
    #     db_data = session.execute(f"SELECT nextval('{CNAEs.__INDEX_SEQUENCE}');")
    #     data = [dict(data) for data in db_data]
    #     return data[0]["nextval"]


def cnaes_repo():
    return CNAEsRepo(CNAEs)
