from envparse import Env

env = Env()

# REAL_DATABASE_URL = env.str(
#     "REAL_DATABASE_URL",
#     default="postgresql+asyncpg://postgres:postgres@0.0.0.0:5432/postgres",
# )

REAL_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default="postgresql+asyncpg://postgres:postgres@db:5432/postgres",
)


APP_PORT = env.int("APP_PORT", default=8000)
