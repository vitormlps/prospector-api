#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from typing import Any, Type, List, Union

# ### Third-party deps
from pydantic import BaseModel
from fastapi import APIRouter, Depends
from sqlalchemy import String
from sqlalchemy.orm import Session

# ### Local deps
from ..security.current_user_auth import get_current_user
from ..database.connection import get_db_local_session
from ..entities.base.repository import CRUDBase
from ..entities.users.model import User


class Relationships:
    def __init__(
        self, router: APIRouter, repository: Any, relationships: List[dict]
    ) -> None:
        self.router = router
        self.repository = repository
        self.relationships = relationships
        self.set_relationships()

    def set_relationships(self):
        for relationship in self.relationships:
            self.get(
                path=relationship["path"],
                repository=self.repository,
                response_model=relationship["response_model"],
            )

            self.get_by_id(
                path=relationship["path"],
                repository=self.repository,
                response_model=relationship["response_model"],
            )

    def get(self, path: str, repository, response_model: Type[List[BaseModel]]):
        operation_name = path.strip("/").replace("/", "_")

        @self.router.get(
            path, response_model=response_model, name=f"Show {operation_name}"
        )
        async def dynamic_route(
            db: Session = Depends(get_db_local_session),
            current_user: User = Depends(get_current_user),
        ):
            return repository.get_all(db)

    def get_by_id(self, path: str, repository: CRUDBase, response_model: Type[BaseModel]):
        operation_name = path.strip("/").replace("/", "_")

        @self.router.get(
            f"/{{id}}{path}",
            response_model=response_model,
            name=f"Get {operation_name} by ID",
        )
        async def get_by_id_route(
            id: Union[int, str],
            db: Session = Depends(get_db_local_session),
            current_user: User = Depends(get_current_user),
        ):
            if isinstance(repository.model.id.type, String):
                id = str(id)
            return repository.get_or_404(db=db, id=id)
