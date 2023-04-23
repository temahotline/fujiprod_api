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


TEST_DATABASE_URL = env.str(
    "TEST_DATABASE_URL",
    default="postgresql+asyncpg://postgres_test:postgres_test@db_tests:5433/postgres_test",
)  # connect string for the test database
