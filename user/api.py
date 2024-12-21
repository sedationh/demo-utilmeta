from utilmeta.core import api, request
from utilmeta.utils import exceptions

from user.schema import SignupSchema, UserSchema, LoginSchema, UserUpdateSchema
from .models import User
from . import auth


@api.CORS(allow_origin="*")
@auth.session_config.plugin
class UserAPI(api.API):
    @api.post
    def signup(self, data: SignupSchema = request.Body) -> UserSchema:
        if User.objects.filter(username=data.username).exists():
            raise exceptions.BadRequest("Username exists")
        data.save()
        auth.user_config.login_user(request=self.request, user=data.get_instance())
        return UserSchema.init(data.pk)

    @api.post
    def login(self, data: LoginSchema = request.Body) -> UserSchema:
        user = auth.user_config.login(
            request=self.request,
            ident=data.username,
            password=data.password,
        )
        if not user:
            raise exceptions.PermissionDenied("Username of password wrong")
        return UserSchema.init(user)

    @api.post
    def logout(self, session: auth.SessionSchema = auth.session_config):
        session.flush()

    def get(self, user: User = auth.user_config) -> UserSchema:
        return UserSchema.init(user)

    def put(
        self, data: UserUpdateSchema = request.Body, user: User = auth.user_config
    ) -> UserSchema:
        data.id = user.pk
        data.save()
        return UserSchema.init(data.pk)
