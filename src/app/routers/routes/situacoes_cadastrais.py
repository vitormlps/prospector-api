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
from ...entities.situacoes_cadastrais.repository import situacoes_cadastrais_repo, SituacoesCadastraisView, SituacoesCadastraisCreate, SituacoesCadastraisUpdate
from ...entities.base.schema import BaseFilter


router = APIRouter(tags=["SituacoesCadastrais"], prefix="/situacoes-cadastrais")


@router.get("", response_model=List[SituacoesCadastraisView])
def get_all_by(
        query: BaseFilter = Depends(BaseFilter),
        current_user: Usuario = Depends(get_current_user),
    ):
    result = situacoes_cadastrais_repo().get_all_by(filters=query)

    if result is None or len(result) == 0:
        raise HTTPException(404, "Situacoes cadastrais not found")

    result = [item for item in result if item.descricao != "-"]

    return result


@router.get("/{id}", response_model=SituacoesCadastraisView)
def get(
        id: UUID, 
        current_user: Usuario = Depends(get_current_user)
    ):
    result = situacoes_cadastrais_repo().get(id)

    if result is None:
        raise HTTPException(404, "Situacao cadastral not found")

    return result
