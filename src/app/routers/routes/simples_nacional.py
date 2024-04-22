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
from ...entities.simples_nacional.repository import simples_nacional_repo, SimplesNacionalView, SimplesNacionalCreate, SimplesNacionalUpdate, SimplesNacionalFilter


router = APIRouter(tags=["SimplesNacional"], prefix="/simples-nacional")


@router.get("", response_model=List[SimplesNacionalView])
def get_all_by(
        query: SimplesNacionalFilter = Depends(SimplesNacionalFilter),
        current_user: Usuario = Depends(get_current_user),
    ):
    result = simples_nacional_repo().get_all_by(filters=query)

    if result is None or len(result) == 0:
        raise HTTPException(404, "Simples nacional not found")

    return result


@router.get("/{id}", response_model=SimplesNacionalView)
def get(
        id: UUID, 
        current_user: Usuario = Depends(get_current_user)
    ):
    result = simples_nacional_repo().get(id)

    if result is None:
        raise HTTPException(404, "Simples nacional not found")

    return result


@router.post("", response_model=SimplesNacionalView)
def create(
        payload: SimplesNacionalCreate,
        current_user: Usuario = Depends(get_current_user)
    ):
    result = simples_nacional_repo().create(payload)

    if result is None:
        raise HTTPException(500, "Simples nacional could not be created")

    return result


@router.put("/{id}", response_model=SimplesNacionalView)
def update(
        id: UUID,
        payload: SimplesNacionalUpdate,
        current_user: Usuario = Depends(get_current_user)
    ):
    result = simples_nacional_repo().update(id=id, obj_in=payload)

    if result is None:
        raise HTTPException(500, "Simples nacional could not be updated")

    return result


@router.delete("/{id}", response_model=SimplesNacionalView)
def delete(
        id: UUID,
        current_user: Usuario = Depends(get_current_user)
    ):
    result = simples_nacional_repo().remove(id)
    
    if not result:
        raise HTTPException(500, "Simples nacional could not be deleted")
    
    return Response(200, "Simples nacional successfully deleted")