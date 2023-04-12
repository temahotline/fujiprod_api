import sentry_sdk
import uvicorn

from fastapi import FastAPI, APIRouter

import settings
from users.router import users_router, licensor_router


# sentry_sdk.init(
#     dsn=settings.SENTRY_URL,
#     traces_sample_rate=1.0,
# )

app = FastAPI(title="fujiprod_api")

main_api_router = APIRouter()

main_api_router.include_router(
    users_router, prefix="/users", tags=["users"],)
main_api_router.include_router(
    licensor_router, prefix="/licensor", tags=["licensor"],)
app.include_router(main_api_router)

if __name__ == "__main__":
    # run app on the host and port
    uvicorn.run(app, host="0.0.0.0", port=settings.APP_PORT)
