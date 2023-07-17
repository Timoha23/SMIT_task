import os

from dotenv import load_dotenv


load_dotenv()


DB_PORT = os.getenv("DB_PORT")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("POSTGRES_DB")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_USER = os.getenv("POSTGRES_USER")

DB_NAME_TEST = os.getenv("POSTGRES_TEST_DB")

DATABASE_URL = (
    f"asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

TEST_DATABASE_URL = (
    f"asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME_TEST}"
)


TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["app.api.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
