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
from ...entities.estabelecimentos.repository import estabelecimentos_repo, EstabelecimentosView, EstabelecimentosCreate, EstabelecimentosUpdate, EstabelecimentosFilter


router = APIRouter(tags=["Estabelecimentos"], prefix="/estabelecimentos")


@router.get("", response_model=List[EstabelecimentosView])
def get_all_by(
        query: EstabelecimentosFilter = Depends(EstabelecimentosFilter),
        current_user: Usuario = Depends(get_current_user),
    ):
    result = estabelecimentos_repo().get_all_by(filters=query)

    if result is None or len(result) == 0:
        raise HTTPException(404, "Estabelecimentos not found")

    return result


@router.get("/{id}", response_model=EstabelecimentosView)
def get(
        id: UUID, 
        current_user: Usuario = Depends(get_current_user)
    ):
    result = estabelecimentos_repo().get(id)

    if result is None:
        raise HTTPException(404, "Estabelecimento not found")

    return result


@router.post("", response_model=EstabelecimentosView)
def create(
        payload: EstabelecimentosCreate,
        current_user: Usuario = Depends(get_current_user)
    ):
    result = estabelecimentos_repo().create(payload)

    if result is None:
        raise HTTPException(500, "Estabelecimento could not be created")

    return result


@router.put("/{id}", response_model=EstabelecimentosView)
def update(
        id: UUID,
        payload: EstabelecimentosUpdate,
        current_user: Usuario = Depends(get_current_user)
    ):
    result = estabelecimentos_repo().update(id=id, obj_in=payload)

    if result is None:
        raise HTTPException(500, "Estabelecimento could not be updated")

    return result


@router.delete("/{id}", response_model=EstabelecimentosView)
def delete(
        id: UUID,
        current_user: Usuario = Depends(get_current_user)
    ):
    result = estabelecimentos_repo().remove(id)
    
    if not result:
        raise HTTPException(500, "Estabelecimento could not be deleted")
    
    return Response(200, "Estabelecimento successfully deleted")