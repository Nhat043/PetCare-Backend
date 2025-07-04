from chalice import Chalice, CORSConfig
from dotenv import load_dotenv
from packages.core.health.routers import health_routers
from packages.v1.roles.routers import roles_routers
from packages.v1.auth.routers import auth_routers
from packages.v1.products.routers import products_routers
from packages.v1.posts.routers import posts_routers

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
auth_routers(app, prefix="/v1/auth", cors=cors_config)
products_routers(app, prefix="/v1/products", cors=cors_config)
posts_routers(app, prefix="/v1/posts", cors=cors_config)
