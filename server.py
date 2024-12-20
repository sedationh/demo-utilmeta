"""
This is a simple one-file project alternative when you setup UtilMeta project
"""

from utilmeta import UtilMeta
from utilmeta.core import api
import os
from utilmeta.ops.config import Operations
from utilmeta.conf.time import Time
from utilmeta.core.orm.databases import DatabaseConnections, Database

import django


@api.CORS(allow_origin="*")
class RootAPI(api.API):
    @api.get
    def hello(self):
        return "world"

    @api.get
    def bmi(self, weight: float, height: float):
        return round(weight / height**2, 1)


production = bool(os.getenv("UTILMETA_PRODUCTION"))
service = UtilMeta(
    __name__,
    name="demo-bmi",
    description="",
    backend=django,
    production=production,
    version=(0, 1, 0),
    host="127.0.0.1",
    port=8000,
    origin="https://demo-bmi.com" if production else None,
    route="/api",
    api=RootAPI,
)


service.use(
    DatabaseConnections(
        {
            "default": Database(
                name="demo-bmi",
                engine="sqlite3",
            )
        }
    )
)
service.use(Time(time_zone="UTC", use_tz=True, datetime_format="%Y-%m-%dT%H:%M:%SZ"))
service.use(
    Operations(
        route="ops",
        database=Database(
            name="demo-bmi_utilmeta_ops",
            engine="sqlite3",
        ),
    )
)


app = service.application()  # used in wsgi/asgi server


if __name__ == "__main__":
    service.run()
    # try: http://127.0.0.1:8000/api/hello
