from decimal import Decimal

from pydantic import BaseModel, Field


class PaymentRequest(BaseModel):
    card_id: int
    amount: Decimal = Field(gt=0)
    currency: str = Field(default="USD", min_length=3, max_length=3)


class PaymentResponse(BaseModel):
    reference_id: str
    status: str
    amount: Decimal
    currency: str
    failure_reason: str | None = None
