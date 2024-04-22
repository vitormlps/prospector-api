#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from typing import List
from uuid import UUID

# ### Third-party deps
from fastapi import APIRouter, Depends, HTTPException, Response

# ### Local deps
from ...security.current_user_auth import get_current_user
from ...entities.usuarios.model import Usuario
from ...entities.faixas_etarias.repository import faixas_etarias_repo, FaixasEtariasView, FaixasEtariasCreate, FaixasEtariasUpdate
from ...entities.base.schema import BaseFilter


router = APIRouter(tags=["FaixasEtarias"], prefix="/faixas-etarias")


@router.get("", response_model=List[FaixasEtariasView])
def get_all_by(
        query: BaseFilter = Depends(BaseFilter),
        current_user: Usuario = Depends(get_current_user),
    ):
    result = faixas_etarias_repo().get_all_by(filters=query)

    if result is None or len(result) == 0:
        raise HTTPException(404, "Faixas etarias not found")

    return result


@router.get("/{id}", response_model=FaixasEtariasView)
def get(
        id: UUID, 
        current_user: Usuario = Depends(get_current_user)
    ):
    result = faixas_etarias_repo().get(id)

    if result is None:
        raise HTTPException(404, "Faixa etaria not found")

    return result
