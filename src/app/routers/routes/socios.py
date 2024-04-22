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
from ...entities.socios.repository import socios_repo, SociosView, SociosCreate, SociosUpdate, SociosFilter


router = APIRouter(tags=["Socios"], prefix="/socios")


@router.get("", response_model=List[SociosView])
def get_all_by(
        query: SociosFilter = Depends(SociosFilter),
        current_user: Usuario = Depends(get_current_user),
    ):
    result = socios_repo().get_all_by(filters=query)

    if result is None or len(result) == 0:
        raise HTTPException(404, "Socios not found")

    return result


@router.get("/{id}", response_model=SociosView)
def get(
        id: UUID, 
        current_user: Usuario = Depends(get_current_user)
    ):
    result = socios_repo().get(id)

    if result is None:
        raise HTTPException(404, "Socio not found")

    return result


@router.post("", response_model=SociosView)
def create(
        payload: SociosCreate,
        current_user: Usuario = Depends(get_current_user)
    ):
    result = socios_repo().create(payload)

    if result is None:
        raise HTTPException(500, "Socio could not be created")

    return result


@router.put("/{id}", response_model=SociosView)
def update(
        id: UUID,
        payload: SociosUpdate,
        current_user: Usuario = Depends(get_current_user)
    ):
    result = socios_repo().update(id=id, obj_in=payload)

    if result is None:
        raise HTTPException(500, "Socio could not be updated")

    return result


@router.delete("/{id}", response_model=SociosView)
def delete(
        id: UUID,
        current_user: Usuario = Depends(get_current_user)
    ):
    result = socios_repo().remove(id)
    
    if not result:
        raise HTTPException(500, "Socio could not be deleted")
    
    return Response(200, "Socio successfully deleted")