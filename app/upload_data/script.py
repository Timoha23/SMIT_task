import asyncio
import os
import json
import datetime

from tortoise import Tortoise, run_async
from pydantic import ValidationError

from app.api.schemas import CargoDetail
from app.settings import TORTOISE_ORM
from app.api.models import TarifDate, Cargo


JSON_DATA_PATH = os.path.join(os.path.dirname(__file__), "data.json")


async def get_or_create_tarif_date(date: str) -> TarifDate:
    datetime.datetime.strptime(date, "%Y-%m-%d")
    tarif_date = await TarifDate.get_or_create(date=date)
    tarif_date = tarif_date[0]
    return tarif_date


async def update_or_create_cargo(
    cargo_data: dict,
    tarif_obj: TarifDate,
) -> Cargo:
    CargoDetail.model_validate(cargo_data)
    cargo_data["type"] = cargo_data["cargo_type"]
    cargo_data["tarif_date"] = tarif_obj
    del cargo_data["cargo_type"]
    cargo = await Cargo.get_or_none(
        type=cargo_data["type"],
        tarif_date=tarif_obj
    )
    if cargo:
        await cargo.update_from_dict(cargo_data).save()
    else:
        cargo = await Cargo.create(**cargo_data)
    return cargo


async def upload_from_json_to_db():
    """
    Внесение данных в БД из .json файла
    """

    errors = {"dates": [], "cargos": []}

    with open(JSON_DATA_PATH) as file:
        data = json.load(file)
        for key, values in data.items():
            try:
                tarif_obj = await get_or_create_tarif_date(key)
            except ValueError:
                errors["dates"].append(key)
                continue
            for value in values:
                try:
                    await update_or_create_cargo(
                        cargo_data=value,
                        tarif_obj=tarif_obj
                    )
                except ValidationError:
                    errors["cargos"].append({key: value})
    if errors["dates"] or errors["cargos"]:
        print("Errors:", errors)


async def init():
    await Tortoise.init(
        config=TORTOISE_ORM
    )

    await Tortoise.generate_schemas()


if __name__ == "__main__":
    run_async(init())
    asyncio.run(upload_from_json_to_db())
