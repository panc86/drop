from fastapi import FastAPI

from api import config, router


app = FastAPI(**config.api_config)
app.include_router(router.app)

