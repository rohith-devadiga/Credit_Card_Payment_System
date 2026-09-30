from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from auth import get_current_user_id
from database import get_db
from payment import process_payment
from schemas import PaymentRequest, PaymentResponse

app = FastAPI(
    title="Payment Processing Service",
    description="Handles payment simulation for the Credit Card Payment System (Module 3).",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/payments/", response_model=PaymentResponse)
def make_payment(
    payload: PaymentRequest,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """
    Initiates a payment: creates a transaction as PENDING, then simulates
    gateway processing to reach a final SUCCESS or FAILED status.
    """
    try:
        txn = process_payment(db, user_id, payload.card_id, payload.amount, payload.currency)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return PaymentResponse(
        reference_id=txn.reference_id,
        status=txn.status,
        amount=txn.amount,
        currency=txn.currency,
        failure_reason=txn.failure_reason or None,
    )
