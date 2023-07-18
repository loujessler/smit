import json
import uvicorn

from datetime import date

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tortoise import models, fields
from tortoise.contrib.fastapi import register_tortoise

from core.config import db_url

app = FastAPI()


class Cargo(BaseModel):
    """
    Class input validation
    """
    cargo_type: str
    declared_cost: float


class Rate(models.Model):
    """
    Class Model rate
    """
    id = fields.IntField(pk=True)
    date = fields.DateField(index=True)
    cargo_type = fields.CharField(50)
    rate = fields.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ("date", "cargo_type")


register_tortoise(
    app,
    db_url=db_url,
    modules={'models': ['main']},
    generate_schemas=True,
    add_exception_handlers=True,
)


@app.on_event("startup")
async def startup_event():
    """
    FastAPI startup func and add all cargos to database from json

    :return:
    """
    await Rate.all().delete()  # delete all existing rates
    try:
        with open('data/rates.json') as f:  # Open json file
            rates_data = json.load(f)

        for rate_date, rates in rates_data.items():  # Cycle for create all objects to database from json
            for rate in rates:
                await Rate.create(date=rate_date, cargo_type=rate["cargo_type"], rate=rate["rate"])
    except FileNotFoundError:
        print("Please add 'rates.json' file to data")


@app.post("/calculate_insurance")
async def calculate_insurance(cargo: Cargo):
    """
    Func calculate insurance for cargo

    :param cargo:
    :return:
    """
    # Search latest insurance
    rate = await Rate.filter(date__lte=date.today(), cargo_type=cargo.cargo_type).order_by('-date').first()
    if rate is None:
        raise HTTPException(status_code=404, detail="No rates available for this cargo type.")

    insurance_cost = cargo.declared_cost * float(rate.rate)
    return {"Insurance Cost": insurance_cost,
            "Latest Insurance": rate.date}


if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8000)
