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
from ...entities.naturezas_juridicas.repository import naturezas_juridicas_repo, NaturezasJuridicasView, NaturezasJuridicasCreate, NaturezasJuridicasUpdate
from ...entities.base.schema import BaseFilter


router = APIRouter(tags=["NaturezasJuridicas"], prefix="/naturezas-juridicas")


@router.get("", response_model=List[NaturezasJuridicasView])
def get_all_by(
        query: BaseFilter = Depends(BaseFilter),
        current_user: Usuario = Depends(get_current_user),
    ):
    result = naturezas_juridicas_repo().get_all_by(filters=query)

    if result is None or len(result) == 0:
        raise HTTPException(404, "Naturezas juridicas not found")

    return result


@router.get("/{id}", response_model=NaturezasJuridicasView)
def get(
        id: UUID, 
        current_user: Usuario = Depends(get_current_user)
    ):
    result = naturezas_juridicas_repo().get(id)

    if result is None:
        raise HTTPException(404, "Natureza juridica not found")

    return result


@router.post("", response_model=NaturezasJuridicasView)
def create(
        payload: NaturezasJuridicasCreate,
        current_user: Usuario = Depends(get_current_user)
    ):
    result = naturezas_juridicas_repo().create(payload)

    if result is None:
        raise HTTPException(500, "Natureza juridica could not be created")

    return result


@router.put("/{id}", response_model=NaturezasJuridicasView)
def update(
        id: UUID,
        payload: NaturezasJuridicasUpdate,
        current_user: Usuario = Depends(get_current_user)
    ):
    result = naturezas_juridicas_repo().update(id=id, obj_in=payload)

    if result is None:
        raise HTTPException(500, "Natureza juridica could not be updated")

    return result


@router.delete("/{id}", response_model=NaturezasJuridicasView)
def delete(
        id: UUID,
        current_user: Usuario = Depends(get_current_user)
    ):
    result = naturezas_juridicas_repo().remove(id)
    
    if not result:
        raise HTTPException(500, "Natureza juridica could not be deleted")
    
    return Response(200, "Natureza juridica successfully deleted")