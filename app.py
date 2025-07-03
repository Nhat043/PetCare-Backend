from chalice import Chalice, CORSConfig
from dotenv import load_dotenv
from packages.core.health.routers import health_routers
from packages.v1.roles.routers import roles_routers

cors_config = CORSConfig(
    allow_origin="*",
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,
    allow_credentials=False,
)

load_dotenv()
app = Chalice(app_name="petcare-backend")
health_routers(app, cors=cors_config)
roles_routers(app, prefix="/v1/roles", cors=cors_config)
