from utilmeta.core import api
from user.api import UserAPI
import utype


class BMISchema(utype.Schema):
    value: float = utype.Field(round=2)

    @property
    def level(self) -> int:
        for i, limit in enumerate([18.5, 25, 30]):
            if self.value < limit:
                return i
        return 3


@api.CORS(allow_origin="*")
class RootAPI(api.API):
    user: UserAPI

    @api.get
    def hello(self):
        return "world"

    @api.get
    def bmi(
        self,
        weight: float = utype.Param(gt=0, le=1000),
        height: float = utype.Param(gt=0, le=4),
    ):
        return BMISchema(value=weight / height**2)
