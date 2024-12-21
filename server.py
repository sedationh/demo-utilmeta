"""
This is a simple one-file project alternative when you setup UtilMeta project
"""

from utilmeta import UtilMeta
import os
from utilmeta.ops.config import Operations
from utilmeta.conf.time import Time
from utilmeta.core.orm.databases import DatabaseConnections, Database
from utilmeta.core.server.backends.django import DjangoSettings

import django


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
    api="api.RootAPI",
    auto_reload=True,
)

service.use(DjangoSettings(secret_key="YOUR_SECRET_KEY", apps=["user"]))

service.use(
    DatabaseConnections(
        {
            "default": Database(
                name="db/demo-bmi",
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
            name="db/demo-bmi_utilmeta_ops",
            engine="sqlite3",
        ),
    )
)


app = service.application()  # used in wsgi/asgi server


if __name__ == "__main__":
    service.run()
    # try: http://127.0.0.1:8000/api/hello
