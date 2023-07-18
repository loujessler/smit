from pydantic import BaseModel
from tortoise import models, fields


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