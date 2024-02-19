from sqlalchemy.orm import Session

from ..entities.base.repository import CRUDBase
from .model import User
from .schema import UserCreate, UserUpdate
from ..utils.encryptors import encrypt_pw


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        obj_in.password = encrypt_pw(obj_in.password)
        db_obj = User(**obj_in.dict())
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        return db_obj


    def update(self, db: Session, *, db_obj: User, obj_in: UserUpdate) -> User:
        obj_in.password = encrypt_pw(obj_in.password)
        return super().update(db=db, db_obj=db_obj, obj_in=obj_in)


user = CRUDUser(User)

