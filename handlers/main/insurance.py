from datetime import date
from fastapi import APIRouter, HTTPException

from db.base import Cargo, Rate

router = APIRouter()


@router.post("/calculate_insurance")
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
