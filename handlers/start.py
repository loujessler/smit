import json
from fastapi import APIRouter

from db.base import Rate
from core.config import refresh_rate

router = APIRouter()


@router.on_event("startup")
async def startup_event():
    """
    FastAPI startup func and add all cargos to database from json

    :return:
    """
    if refresh_rate:
        await Rate.all().delete()  # delete all existing rates
        try:
            with open('./data/rates.json') as f:  # Open json file
                rates_data = json.load(f)

            for rate_date, rates in rates_data.items():  # Cycle for create all objects to database from json
                for rate in rates:
                    await Rate.create(date=rate_date, cargo_type=rate["cargo_type"], rate=rate["rate"])
        except FileNotFoundError:
            print("Please add 'rates.json' file to data")
