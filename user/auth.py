from utilmeta.core import auth
from utilmeta.core.auth.session.db import DBSessionSchema, DBSession
from .models import Session, User

USER_ID = "_user_id"

# 假设会话数据存储在数据库或 Cookie 中，格式如下：
# session_data = {
#     "_user_id": 123,  # 用户 ID
#     "session_id": "abc123",  # 会话 ID
#     "data": "some_session_data",  # 其他会话数据
# }


class SessionSchema(DBSessionSchema):
    def get_session_data(self):
        data = super().get_session_data()
        data.update(user_id=self.get(USER_ID))
        return data


session_config = DBSession(
    session_model=Session,
    engine=SessionSchema,
    cookie=DBSession.Cookie(name="sessionid", age=7 * 24 * 3600, http_only=True),
)

user_config = auth.User(
    user_model=User,
    authentication=session_config,
    key=USER_ID,
    login_fields=User.username,
    password_field=User.password,
)
