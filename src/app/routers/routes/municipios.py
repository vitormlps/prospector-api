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
from ...entities.municipios.repository import municipios_repo, MunicipiosView, MunicipiosCreate, MunicipiosUpdate
from ...entities.base.schema import BaseFilter


router = APIRouter(tags=["Municipios"], prefix="/municipios")


@router.get("", response_model=List[MunicipiosView])
def get_all_by(
        query: BaseFilter = Depends(BaseFilter),
        current_user: Usuario = Depends(get_current_user),
    ):
    result = municipios_repo().get_all_by(filters=query)

    if result is None or len(result) == 0:
        raise HTTPException(404, "Municipios not found")

    return result


@router.get("/{id}", response_model=MunicipiosView)
def get(
        id: UUID, 
        current_user: Usuario = Depends(get_current_user)
    ):
    result = municipios_repo().get(id)

    if result is None:
        raise HTTPException(404, "Municipio not found")

    return result


@router.post("", response_model=MunicipiosView)
def create(
        payload: MunicipiosCreate,
        current_user: Usuario = Depends(get_current_user)
    ):
    result = municipios_repo().create(payload)

    if result is None:
        raise HTTPException(500, "Municipio could not be created")

    return result


@router.put("/{id}", response_model=MunicipiosView)
def update(
        id: UUID,
        payload: MunicipiosUpdate,
        current_user: Usuario = Depends(get_current_user)
    ):
    result = municipios_repo().update(id=id, obj_in=payload)

    if result is None:
        raise HTTPException(500, "Municipio could not be updated")

    return result


@router.delete("/{id}", response_model=MunicipiosView)
def delete(
        id: UUID,
        current_user: Usuario = Depends(get_current_user)
    ):
    result = municipios_repo().remove(id)
    
    if not result:
        raise HTTPException(500, "Municipio could not be deleted")
    
    return Response(200, "Municipio successfully deleted")