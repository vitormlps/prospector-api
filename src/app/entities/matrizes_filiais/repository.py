#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
# ### Local deps
from ...entities.base.repository import BaseRepo
from .model import MatrizFilial
from .schema import MatrizesFiliaisView, MatrizesFiliaisCreate, MatrizesFiliaisUpdate


class MatrizesFiliaisRepo(BaseRepo[MatrizFilial, MatrizesFiliaisCreate, MatrizesFiliaisUpdate]):
    pass


def matrizes_filiais_repo():
    return MatrizesFiliaisRepo(MatrizFilial)
