import pytest
from secure_api import Transaction, validate_and_sort_transactions

def test_sqli_injection_attempt_rejected():
    txs = [
        Transaction(id=1, amount=100.0, status="COMPLETED", tenant_id="org_1"),
    ]
    
    # Malicious injection string
    malicious_sort = "amount; DROP TABLE transactions;--"
    
    with pytest.raises(ValueError, match="Invalid sort parameter"):
        validate_and_sort_transactions(txs, "org_1", malicious_sort)
