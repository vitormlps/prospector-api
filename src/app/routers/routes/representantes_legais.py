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
from ...entities.representantes_legais.repository import representantes_legais_repo, RepresentantesLegaisView, RepresentantesLegaisCreate, RepresentantesLegaisUpdate, RepresentantesLegaisFilter


router = APIRouter(tags=["RepresentantesLegais"], prefix="/representantes-legais")


@router.get("", response_model=List[RepresentantesLegaisView])
def get_all_by(
        query: RepresentantesLegaisFilter = Depends(RepresentantesLegaisFilter),
        current_user: Usuario = Depends(get_current_user),
    ):
    result = representantes_legais_repo().get_all_by(filters=query)

    if result is None or len(result) == 0:
        raise HTTPException(404, "Representantes legais not found")

    return result


@router.get("/{id}", response_model=RepresentantesLegaisView)
def get(
        id: UUID, 
        current_user: Usuario = Depends(get_current_user)
    ):
    result = representantes_legais_repo().get(id)

    if result is None:
        raise HTTPException(404, "Representante legal not found")

    return result


@router.post("", response_model=RepresentantesLegaisView)
def create(
        payload: RepresentantesLegaisCreate,
        current_user: Usuario = Depends(get_current_user)
    ):
    result = representantes_legais_repo().create(payload)

    if result is None:
        raise HTTPException(500, "Representante legal could not be created")

    return result


@router.put("/{id}", response_model=RepresentantesLegaisView)
def update(
        id: UUID,
        payload: RepresentantesLegaisUpdate,
        current_user: Usuario = Depends(get_current_user)
    ):
    result = representantes_legais_repo().update(id=id, obj_in=payload)

    if result is None:
        raise HTTPException(500, "Representante legal could not be updated")

    return result


@router.delete("/{id}", response_model=RepresentantesLegaisView)
def delete(
        id: UUID,
        current_user: Usuario = Depends(get_current_user)
    ):
    result = representantes_legais_repo().remove(id)
    
    if not result:
        raise HTTPException(500, "Representante legal could not be deleted")
    
    return Response(200, "Representante legal successfully deleted")