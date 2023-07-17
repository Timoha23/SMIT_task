import decimal
from typing import Dict, List

from pydantic import BaseModel, Field, RootModel


class CargoDetail(BaseModel):
    """
    Модель данных для получения информации о грузах
    """

    cargo_type: str = Field(alias="type")
    rate: float

    class Config:
        from_attributes = True
        populate_by_name = True


class GetTarif(RootModel):
    """
    Модель данных для получения даты и деталей о грузах,
    в данную дату
    """

    root: Dict[str, List[CargoDetail]]


class CalculateInsurancePrice(BaseModel):
    """
    Модель данных для расчета стоимости страховки
    """

    date: str = None
    cargo_type: str
    declared_price: decimal.Decimal


class GetInsurancePrice(BaseModel):
    """
    Модель данных для получения стоимости страховки
    """

    date: str
    insurance_price: float
    declared_price: float
    cargo: CargoDetail
