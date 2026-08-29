import sys
import os
from decimal import Decimal
from hypothesis import given, strategies as st
import pytest
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ch02_bulletproof_spec")))
from transfer_service import BankLedger

@given(
    initial_a=st.decimals(min_value=100, max_value=10000, places=2),
    initial_b=st.decimals(min_value=100, max_value=10000, places=2),
    transfer_amount=st.decimals(min_value=1, max_value=500, places=2)
)
def test_hypothesis_conservation_of_mass(initial_a, initial_b, transfer_amount):
    ledger = BankLedger()
    ledger.set_balance("ACC_A", initial_a)
    ledger.set_balance("ACC_B", initial_b)
    
    total_before = ledger.get_total_balance()
    asyncio.run(ledger.transfer("ACC_A", "ACC_B", transfer_amount))
    total_after = ledger.get_total_balance()

    assert total_after == total_before
