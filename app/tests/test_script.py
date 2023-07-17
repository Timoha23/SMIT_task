from app.tests.conftest import (
    get_count_cargos,
    get_cargo,
    get_count_tarifs
)
from app.upload_data.script import (
    get_or_create_tarif_date,
    update_or_create_cargo
)


async def test_create_tarif_date():
    """
    Тест создание даты для тарифов
    """

    count_tarifs_before_create = await get_count_tarifs()

    await get_or_create_tarif_date("2022-01-01")
    await get_or_create_tarif_date("2022-01-02")
    # like a tarif_obj_1 (+0)
    await get_or_create_tarif_date("2022-01-01")

    count_tarifs_after_create = await get_count_tarifs()

    assert count_tarifs_before_create + 2 == count_tarifs_after_create


async def test_create_cargo():
    """
    Тест создание грузов
    """

    count_cargos_before_create = await get_count_cargos()

    tarif_obj_1 = await get_or_create_tarif_date("2022-01-01")
    tarif_obj_2 = await get_or_create_tarif_date("2022-01-02")

    cargo_1 = await update_or_create_cargo(
        cargo_data={"cargo_type": "Glass", "rate": 0.02},
        tarif_obj=tarif_obj_1,
    )
    cargo_2 = await update_or_create_cargo(
        cargo_data={"cargo_type": "Glass", "rate": 0.02},
        tarif_obj=tarif_obj_2,
    )
    # like a cargo_1, but different types (+1)
    cargo_3 = await update_or_create_cargo(
        cargo_data={"cargo_type": "Other", "rate": 0.02},
        tarif_obj=tarif_obj_1,
    )
    # like a cargo_1 (+0)
    cargo_4 = await update_or_create_cargo(
        cargo_data={"cargo_type": "Glass", "rate": 0.02},
        tarif_obj=tarif_obj_1,
    )
    # like a cargo_1, but different rates (+0)
    cargo_5 = await update_or_create_cargo(
        cargo_data={"cargo_type": "Glass", "rate": 0.025},
        tarif_obj=tarif_obj_1,
    )

    cargo_1 = await get_cargo(id=cargo_1.id)

    count_cargos_after_create = await get_count_cargos()

    assert cargo_1.rate == cargo_5.rate
    assert cargo_1.id == cargo_5.id == cargo_4.id != cargo_2.id != cargo_3.id
    assert count_cargos_before_create + 3 == count_cargos_after_create
