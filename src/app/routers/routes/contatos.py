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
from ...entities.contatos.repository import contatos_repo, ContatosView, ContatosCreate, ContatosUpdate, ContatosFilter


router = APIRouter(tags=["Contatos"], prefix="/contatos")


@router.get("", response_model=List[ContatosView])
def get_all_by(
        query: ContatosFilter = Depends(ContatosFilter),
        current_user: Usuario = Depends(get_current_user),
    ):
    result = contatos_repo().get_all_by(filters=query)

    if result is None or len(result) == 0:
        raise HTTPException(404, "Contatos not found")

    return result


@router.get("/{id}", response_model=ContatosView)
def get(
        id: UUID, 
        current_user: Usuario = Depends(get_current_user)
    ):
    result = contatos_repo().get(id)

    if result is None:
        raise HTTPException(404, "Contato not found")

    return result


@router.post("", response_model=ContatosView)
def create(
        payload: ContatosCreate,
        current_user: Usuario = Depends(get_current_user)
    ):
    result = contatos_repo().create(payload)

    if result is None:
        raise HTTPException(500, "Contato could not be created")

    return result


@router.put("/{id}", response_model=ContatosView)
def update(
        id: UUID,
        payload: ContatosUpdate,
        current_user: Usuario = Depends(get_current_user)
    ):
    result = contatos_repo().update(id=id, obj_in=payload)

    if result is None:
        raise HTTPException(500, "Contato could not be updated")

    return result


@router.delete("/{id}", response_model=ContatosView)
def delete(
        id: UUID,
        current_user: Usuario = Depends(get_current_user)
    ):
    result = contatos_repo().remove(id)
    
    if not result:
        raise HTTPException(500, "Contato could not be deleted")
    
    return Response(200, "Contato successfully deleted")