from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "tarifdate" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "date" VARCHAR(10) NOT NULL UNIQUE,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE "tarifdate" IS 'Модель даты тарифов';
CREATE TABLE IF NOT EXISTS "cargo" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "type" VARCHAR(100) NOT NULL,
    "rate" DECIMAL(4,4) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "tarif_date_id" INT NOT NULL REFERENCES "tarifdate" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "cargo" IS 'Модель груза';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
