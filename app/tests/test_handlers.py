from httpx import AsyncClient

from app.upload_data.script import (
    get_or_create_tarif_date,
    update_or_create_cargo
)


async def test_get_price(
    async_client: AsyncClient,
):
    """
    Тест эндпоинта получение стоимости страхового тарифа
    """

    RATE_1 = 0.1
    RATE_2 = 0.2
    DECLARED_PRICE = 100

    tarif_obj_1 = await get_or_create_tarif_date(date="2030-01-01")
    tarif_obj_2 = await get_or_create_tarif_date(date="2030-02-01")

    cargo_data_1 = {"cargo_type": "Glass", "rate": RATE_1}
    cargo_data_2 = {"cargo_type": "Glass", "rate": RATE_2}
    cargo_1 = await update_or_create_cargo(
        cargo_data=cargo_data_1,
        tarif_obj=tarif_obj_1,
    )

    cargo_2 = await update_or_create_cargo(
        cargo_data=cargo_data_2,
        tarif_obj=tarif_obj_2,
    )

    # BODIES
    body_with_all_data = {
        "date": tarif_obj_1.date,
        "cargo_type": cargo_1.type,
        "declared_price": DECLARED_PRICE
    }
    body_without_date = {
        "cargo_type": cargo_1.type,
        "declared_price": DECLARED_PRICE
    }
    body_without_cargo_type = {
        "date": tarif_obj_1.date,
        "declared_price": DECLARED_PRICE
    }
    body_without_declared_price = {
        "date": tarif_obj_1.date,
        "cargo_type": cargo_1.type,
    }

    # RESPONSES
    # g_r - good response
    # b_r - bad response
    g_r = await async_client.post(
        url="/get_price/",
        json=body_with_all_data,
    )
    g_r_without_date = await async_client.post(
        url="/get_price/",
        json=body_without_date,
    )
    b_r_without_cargo_type = await async_client.post(
        url="/get_price/",
        json=body_without_cargo_type,
    )
    b_r_without_declared_price = await async_client.post(
        url="/get_price/",
        json=body_without_declared_price
    )

    # ASSERTS
    assert g_r.status_code == 200
    assert g_r.json()["insurance_price"] == DECLARED_PRICE * RATE_1
    assert g_r.json()["date"] == tarif_obj_1.date
    assert g_r.json()["declared_price"] == DECLARED_PRICE
    assert g_r.json()["cargo"]["type"] == cargo_1.type
    assert g_r.json()["cargo"]["rate"] == float(cargo_1.rate)

    assert g_r_without_date.status_code == 200
    assert g_r_without_date.json()["insurance_price"] == (
        DECLARED_PRICE * RATE_2
    )
    assert g_r_without_date.json()["date"] == tarif_obj_2.date
    assert g_r_without_date.json()["declared_price"] == DECLARED_PRICE
    assert g_r_without_date.json()["cargo"]["type"] == cargo_2.type
    assert g_r_without_date.json()["cargo"]["rate"] == float(cargo_2.rate)

    assert b_r_without_cargo_type.status_code == 422
    assert b_r_without_declared_price.status_code == 422
