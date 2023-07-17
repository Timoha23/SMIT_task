from tortoise import fields, models


class TarifDate(models.Model):
    """
    Модель даты тарифов
    """

    id = fields.IntField(pk=True)
    date = fields.CharField(max_length=10, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)


class Cargo(models.Model):
    """
    Модель груза
    """

    id = fields.IntField(pk=True)
    type = fields.CharField(max_length=100, uniqie=True)
    rate = fields.DecimalField(max_digits=4, decimal_places=4)
    tarif_date = fields.ForeignKeyField(
        model_name="models.TarifDate",
        related_name="cargo",
        on_delete="CASCADE"
    )
    created_at = fields.DatetimeField(auto_now_add=True)
