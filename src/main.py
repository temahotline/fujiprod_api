import sentry_sdk
import uvicorn

from fastapi import FastAPI, APIRouter
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from src import settings
from src.users.router import users_router
from src.licensor.router import licensor_router
from src.releases.router import releases_router
from src.tracks.router import tracks_router
from src.orders.router import order_router


# sentry_sdk.init(
#     dsn=settings.SENTRY_URL,
#     traces_sample_rate=1.0,
# )

print(f"REAL_DATABASE_URL: {settings.REAL_DATABASE_URL}")

app = FastAPI(title="fujiprod_api")

main_api_router = APIRouter()

main_api_router.include_router(
    users_router, prefix="/users", tags=["users"],)
main_api_router.include_router(
    licensor_router, prefix="/licensor", tags=["licensor"],)
main_api_router.include_router(
    releases_router, prefix="/releases", tags=["releases"],)
main_api_router.include_router(
    tracks_router, prefix="/tracks", tags=["tracks"]
)
main_api_router.include_router(
    order_router, prefix="/orders", tags=["orders"]
)
app.include_router(main_api_router)


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


if __name__ == "__main__":
    # run app on the host and port
    uvicorn.run(app, host="0.0.0.0", port=settings.APP_PORT)
