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
from ...entities.paises.repository import paises_repo, PaisesView, PaisesCreate, PaisesUpdate
from ...entities.base.schema import BaseFilter


router = APIRouter(tags=["Paises"], prefix="/paises")


@router.get("", response_model=List[PaisesView])
def get_all_by(
        query: BaseFilter = Depends(BaseFilter),
        current_user: Usuario = Depends(get_current_user),
    ):
    result = paises_repo().get_all_by(filters=query)

    if result is None or len(result) == 0:
        raise HTTPException(404, "Paises not found")

    return result


@router.get("/{id}", response_model=PaisesView)
def get(
        id: UUID, 
        current_user: Usuario = Depends(get_current_user)
    ):
    result = paises_repo().get(id)

    if result is None:
        raise HTTPException(404, "Pais not found")

    return result


@router.post("", response_model=PaisesView)
def create(
        payload: PaisesCreate,
        current_user: Usuario = Depends(get_current_user)
    ):
    result = paises_repo().create(payload)

    if result is None:
        raise HTTPException(500, "Pais could not be created")

    return result


@router.put("/{id}", response_model=PaisesView)
def update(
        id: UUID,
        payload: PaisesUpdate,
        current_user: Usuario = Depends(get_current_user)
    ):
    result = paises_repo().update(id=id, obj_in=payload)

    if result is None:
        raise HTTPException(500, "Pais could not be updated")

    return result


@router.delete("/{id}", response_model=PaisesView)
def delete(
        id: UUID,
        current_user: Usuario = Depends(get_current_user)
    ):
    result = paises_repo().remove(id)
    
    if not result:
        raise HTTPException(500, "Pais could not be deleted")
    
    return Response(200, "Pais successfully deleted")