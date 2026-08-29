import pytest
import asyncio
from decimal import Decimal
from transfer_service import BankLedger

@pytest.mark.asyncio
async def test_conservation_of_mass_under_concurrency():
    ledger = BankLedger()
    ledger.set_balance("ACC_A", Decimal("1000.00"))
    ledger.set_balance("ACC_B", Decimal("1000.00"))
    initial_total = ledger.get_total_balance()

    # Simulate 50 concurrent transactions between accounts
    tasks = [
        ledger.transfer("ACC_A", "ACC_B", Decimal("10.00")),
        ledger.transfer("ACC_B", "ACC_A", Decimal("15.00")),
        ledger.transfer("ACC_A", "ACC_B", Decimal("5.00")),
    ] * 15

    await asyncio.gather(*tasks)

    # INVARIANT: Total currency in circulation MUST remain constant
    final_total = ledger.get_total_balance()
    assert final_total == initial_total, f"Mass violation: Expected {initial_total}, got {final_total}"
