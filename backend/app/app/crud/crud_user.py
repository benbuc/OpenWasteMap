from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_by_nickname(self, db: Session, *, nickname: str) -> Optional[User]:
        return db.query(User).filter(User.nickname == nickname).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email.lower(),
            nickname=obj_in.nickname.lower(),
            hashed_password=get_password_hash(obj_in.password),
            date_joined=datetime.utcnow(),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if "password" in update_data:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        if "email" in update_data and update_data["email"] != db_obj.email:
            update_data["email_verified"] = False
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def update_email_verified(
        self, db: Session, *, db_obj: User, new_email_verified: bool
    ) -> User:
        update_data = {"email_verified": new_email_verified}
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def update_is_superuser(
        self, db: Session, *, db_obj: User, new_is_superuser: bool
    ) -> User:
        update_data = {"is_superuser": new_is_superuser}
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser

    def is_email_verified(self, user: User) -> bool:
        return user.email_verified

    def get_all(self, db: Session) -> List[User]:
        return db.query(User).all()


user = CRUDUser(User)
