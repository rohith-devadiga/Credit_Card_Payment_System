from unittest.mock import MagicMock

import pytest

from payment import process_payment, simulate_gateway_call


def test_simulate_gateway_deterministic_failure():
    status, reason = simulate_gateway_call(0.01)
    assert status == "FAILED"
    assert reason


def test_process_payment_card_not_found():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None
    with pytest.raises(ValueError):
        process_payment(db, user_id=1, card_id=999, amount=10, currency="USD")


def test_process_payment_success_flow(monkeypatch):
    db = MagicMock()
    fake_card = MagicMock(id=1, user_id=1)
    db.query.return_value.filter.return_value.first.return_value = fake_card

    monkeypatch.setattr("payment.simulate_gateway_call", lambda amount: ("SUCCESS", ""))

    txn = process_payment(db, user_id=1, card_id=1, amount=25.00, currency="USD")
    assert txn.status == "SUCCESS"
    assert db.add.called
    assert db.commit.call_count >= 2
