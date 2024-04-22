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
from ...entities.qualificacoes.repository import qualificacoes_repo, QualificacoesView, QualificacoesCreate, QualificacoesUpdate
from ...entities.base.schema import BaseFilter


router = APIRouter(tags=["Qualificacoes"], prefix="/qualificacoes")


@router.get("", response_model=List[QualificacoesView])
def get_all_by(
        query: BaseFilter = Depends(BaseFilter),
        current_user: Usuario = Depends(get_current_user),
    ):
    result = qualificacoes_repo().get_all_by(filters=query)

    if result is None or len(result) == 0:
        raise HTTPException(404, "Qualificacoes not found")

    return result


@router.get("/{id}", response_model=QualificacoesView)
def get(
        id: UUID, 
        current_user: Usuario = Depends(get_current_user)
    ):
    result = qualificacoes_repo().get(id)

    if result is None:
        raise HTTPException(404, "Qualificacao not found")

    return result


@router.post("", response_model=QualificacoesView)
def create(
        payload: QualificacoesCreate,
        current_user: Usuario = Depends(get_current_user)
    ):
    result = qualificacoes_repo().create(payload)

    if result is None:
        raise HTTPException(500, "Qualificacao could not be created")

    return result


@router.put("/{id}", response_model=QualificacoesView)
def update(
        id: UUID,
        payload: QualificacoesUpdate,
        current_user: Usuario = Depends(get_current_user)
    ):
    result = qualificacoes_repo().update(id=id, obj_in=payload)

    if result is None:
        raise HTTPException(500, "Qualificacao could not be updated")

    return result


@router.delete("/{id}", response_model=QualificacoesView)
def delete(
        id: UUID,
        current_user: Usuario = Depends(get_current_user)
    ):
    result = qualificacoes_repo().remove(id)
    
    if not result:
        raise HTTPException(500, "Qualificacao could not be deleted")
    
    return Response(200, "Qualificacao successfully deleted")