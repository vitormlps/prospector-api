from ..entities.base.repository import CRUDBase
from .model import UserType
from .schema import UserTypeCreate, UserTypeUpdate


class CRUDUserType(CRUDBase[UserType, UserTypeCreate, UserTypeUpdate]):
    pass


user_type = CRUDUserType(UserType)
