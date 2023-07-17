# SMIT_task
Миграции:
1. aerich init -t app.settings.TORTOISE_ORM
2. aerich init-db
3. if have changes aerich migrate --name drop_column
4. aerich upgrade