from datetime import datetime
from utilmeta.core import api, orm, request
from utilmeta.utils import exceptions
from .models import User
from . import auth


class SignupSchema(orm.Schema[User]):
    username: str
    password: str


class UserSchema(orm.Schema[User]):
    id: int
    username: str
    signup_time: datetime


@auth.session_config.plugin
class UserAPI(api.API):
    @api.post
    def signup(self, data: SignupSchema = request.Body) -> UserSchema:
        if User.objects.filter(username=data.username).exists():
            raise exceptions.BadRequest("Username exists")
        data.save()
        auth.user_config.login_user(request=self.request, user=data.get_instance())
        return UserSchema.init(data.pk)
