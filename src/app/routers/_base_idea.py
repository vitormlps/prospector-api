#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from typing import List, Any, TypeVar

# ### Third-party deps
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# ### Local deps
from app.security.authentication import get_current_user, get_entity_type, get_db
from app.entities.base.model import Base


EntityType = TypeVar("EntityType", bound=Base)
EntityTypeBase = TypeVar("EntityTypeBase", bound=Base)
EntityTypeCreate = TypeVar("EntityTypeCreate", bound=Base)
EntityTypeUpdate = TypeVar("EntityTypeUpdate", bound=Base)


class EntityRouter:
    def __init__(self, _tags: str, _prefix: str, routes) -> None:
        self.api_router = APIRouter(tags=[_tags], prefix=_prefix)
        self.add_routes(routes)


    def add_routes(self, routes):
        for route in routes:
            _endpoint = None

            match route.methods[0]:
                case "GET":

                    if ["/{", "id}"] in route.path:
                        _endpoint = self.get
                    else:
                        _endpoint = self.get_all_by

                case "POST":
                    _endpoint = self.create

                case "PUT":
                    _endpoint = self.update

                case "DELETE":
                    _endpoint = self.delete


            self.api_router.add_api_route(
                path=route.path, 
                enpoint=_endpoint, 
                methods=route.methods, 
                response_model=route.response_model, 
                # dependencies=route.dependencies
            )

    
    def get_all_by(self, 
                # entity: EntityType, 
                payload: EntityTypeBase,
                entity: EntityType = Depends(get_entity_type), 
                db: Session = Depends(get_db), 
                current_user = Depends(get_current_user)
        ):
        entity.get_all_by(db=db)


    def get(self, 
                id: str,
                entity: EntityType = Depends(get_entity_type), 
                db: Session = Depends(get_db), 
                current_user = Depends(get_current_user)
        ):
        entity.get(db=db, id=id)


    def create(self, 
                payload: EntityTypeCreate,
                # entity: EntityType, 
                entity: EntityType = Depends(get_entity_type), 
                db: Session = Depends(get_db), 
                current_user = Depends(get_current_user)
        ):
        entity.create(db=db, obj_in=payload)


    def update(self, 
                payload: EntityTypeUpdate,
                entity: EntityType = Depends(get_entity_type), 
                db: Session = Depends(get_db), 
                current_user = Depends(get_current_user)
        ):
        entity.update(db=db, id=id, obj_in=payload)


    def delete(self, 
                id: str,
                entity: EntityType = Depends(get_entity_type), 
                db: Session = Depends(get_db), 
                current_user = Depends(get_current_user)
        ):
        entity.delete(db=db, id=id)
