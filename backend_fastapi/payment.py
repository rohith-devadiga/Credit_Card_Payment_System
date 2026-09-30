import random
import uuid

from sqlalchemy.orm import Session

from models import Card, Transaction


def simulate_gateway_call(amount) -> tuple[str, str]:
    """
    Simulates a call to an external payment gateway.
    Fails ~15% of the time, or always fails for the well-known test
    amount 0.01 so failure handling can be demoed/tested deterministically.
    """
    if amount == 0.01:
        return "FAILED", "Card declined by issuer."
    if random.random() < 0.15:
        return "FAILED", "Payment gateway timeout."
    return "SUCCESS", ""


def process_payment(db: Session, user_id: int, card_id: int, amount, currency: str) -> Transaction:
    card = db.query(Card).filter(Card.id == card_id, Card.user_id == user_id).first()
    if card is None:
        raise ValueError("Card not found for this user.")

    # Step 1: create the transaction in PENDING state.
    txn = Transaction(
        reference_id=uuid.uuid4().hex,
        user_id=user_id,
        card_id=card_id,
        amount=amount,
        currency=currency,
        status="PENDING",
    )
    db.add(txn)
    db.commit()
    db.refresh(txn)

    # Step 2: simulate processing and move to a final status.
    final_status, reason = simulate_gateway_call(float(amount))
    txn.status = final_status
    txn.failure_reason = reason
    db.commit()
    db.refresh(txn)
    return txn
