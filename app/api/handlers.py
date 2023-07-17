from fastapi import APIRouter, HTTPException

from app.api.models import TarifDate, Cargo
from app.api.schemas import (
    GetTarif,
    GetInsurancePrice,
    CalculateInsurancePrice
)


main_router = APIRouter()


@main_router.get(
    "/",
    status_code=200,
    response_model=list[GetTarif],
    response_model_by_alias=False
)
async def get_all_insurance_data():
    """
    Получение всех дат со всеми тарифами
    """

    tarifs = await TarifDate.all().prefetch_related("cargo")
    return [GetTarif({tarif.date: list(tarif.cargo)}) for tarif in tarifs]


@main_router.post(
    "/get_price/",
    status_code=200,
    response_model=GetInsurancePrice
)
async def get_insurance_price(
    body: CalculateInsurancePrice,
):
    """
    Получение стоимости страхового тарифа
    """

    # Если в теле запроса дата не указана, то
    # берем самую "свежую" дату
    if body.date is None:
        cargo = await (
            Cargo.filter(type=body.cargo_type)
            .select_related("tarif_date")
            .order_by("-tarif_date__date")
            .first()
        )
    else:
        cargo = await Cargo.get_or_none(
            type=body.cargo_type,
            tarif_date__date=body.date,
        ).select_related("tarif_date")

    if cargo is None:
        raise HTTPException(
            status_code=404,
            detail="Информация по страхованию о грузе с"
                   " данными параметрами не найдена."
        )

    insurance_price = cargo.rate * body.declared_price
    return GetInsurancePrice(
        insurance_price=insurance_price,
        declared_price=body.declared_price,
        date=cargo.tarif_date.date,
        cargo=cargo
    )
