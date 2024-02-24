#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
# ### Local deps
from ...entities.base.repository import BaseRepo
from .model import RepresentanteLegal
from .schema import RepresentantesLegaisView, RepresentantesLegaisCreate, RepresentantesLegaisUpdate


class RepresentantesLegaisRepo(BaseRepo[RepresentanteLegal, RepresentantesLegaisCreate, RepresentantesLegaisUpdate]):
    pass


def RepresentantesLegais_repo():
    return RepresentantesLegaisRepo(RepresentanteLegal)
