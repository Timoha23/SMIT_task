import uvicorn
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.api.handlers import main_router
from app.settings import TORTOISE_ORM


app = FastAPI(title="Insurance service")

app.include_router(main_router)

if __name__ == "__main__":
    register_tortoise(
        app=app,
        config=TORTOISE_ORM,
        generate_schemas=True,
        add_exception_handlers=True,
    )
    uvicorn.run(app, host="127.0.0.1", port=8000)
