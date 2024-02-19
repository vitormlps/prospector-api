#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
# ### Local deps
from ...entities.base.repository import BaseRepo
from .model import Motivos
from .schema import MotivosView, MotivosCreate, MotivosUpdate


class MotivosRepo(BaseRepo[Motivos, MotivosCreate, MotivosUpdate]):
    pass


def motivos_repo():
    return MotivosRepo(Motivos)
