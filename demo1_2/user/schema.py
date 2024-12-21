from datetime import datetime
from utilmeta.core import orm
import utype
from user.models import User


class SignupSchema(orm.Schema[User]):
    username: str
    password: str


class UserSchema(orm.Schema[User]):
    id: int
    username: str
    signup_time: datetime


class LoginSchema(utype.Schema):
    username: str
    password: str


class UserUpdateSchema(orm.Schema[User]):
    id: int = orm.Field(no_input=True)
    username: str = orm.Field(required=False)
    password: str = orm.Field(required=False)
