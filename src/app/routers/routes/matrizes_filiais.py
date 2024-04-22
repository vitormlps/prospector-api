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
from ...entities.matrizes_filiais.repository import matrizes_filiais_repo, MatrizesFiliaisView, MatrizesFiliaisCreate, MatrizesFiliaisUpdate
from ...entities.base.schema import BaseFilter


router = APIRouter(tags=["MatrizesFiliais"], prefix="/matriz-filiais")


@router.get("", response_model=List[MatrizesFiliaisView])
def get_all_by(
        query: BaseFilter = Depends(BaseFilter),
        current_user: Usuario = Depends(get_current_user),
    ):
    result = matrizes_filiais_repo().get_all_by(filters=query)

    if result is None or len(result) == 0:
        raise HTTPException(404, "Matrizes filiais not found")

    return result


@router.get("/{id}", response_model=MatrizesFiliaisView)
def get(
        id: UUID, 
        current_user: Usuario = Depends(get_current_user)
    ):
    result = matrizes_filiais_repo().get(id)

    if result is None:
        raise HTTPException(404, "Matriz filial not found")

    return result
