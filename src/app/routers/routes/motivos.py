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
from ...entities.motivos.repository import motivos_repo, MotivosView, MotivosCreate, MotivosUpdate
from ...entities.base.schema import BaseFilter


router = APIRouter(tags=["Motivos"], prefix="/motivos")


@router.get("", response_model=List[MotivosView])
def get_all_by(
        query: BaseFilter = Depends(BaseFilter),
        current_user: Usuario = Depends(get_current_user),
    ):
    result = motivos_repo().get_all_by(filters=query)

    if result is None or len(result) == 0:
        raise HTTPException(404, "Motivos not found")

    return result


@router.get("/{id}", response_model=MotivosView)
def get(
        id: UUID, 
        current_user: Usuario = Depends(get_current_user)
    ):
    result = motivos_repo().get(id)

    if result is None:
        raise HTTPException(404, "Motivo not found")

    return result


@router.post("", response_model=MotivosView)
def create(
        payload: MotivosCreate,
        current_user: Usuario = Depends(get_current_user)
    ):
    result = motivos_repo().create(payload)

    if result is None:
        raise HTTPException(500, "Motivo could not be created")

    return result


@router.put("/{id}", response_model=MotivosView)
def update(
        id: UUID,
        payload: MotivosUpdate,
        current_user: Usuario = Depends(get_current_user)
    ):
    result = motivos_repo().update(id=id, obj_in=payload)

    if result is None:
        raise HTTPException(500, "Motivo could not be updated")

    return result


@router.delete("/{id}", response_model=MotivosView)
def delete(
        id: UUID,
        current_user: Usuario = Depends(get_current_user)
    ):
    result = motivos_repo().remove(id)
    
    if not result:
        raise HTTPException(500, "Motivo could not be deleted")
    
    return Response(200, "Motivo successfully deleted")