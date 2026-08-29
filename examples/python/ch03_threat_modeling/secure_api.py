from typing import List, Set
from pydantic import BaseModel

ALLOWED_SORT_COLUMNS: Set[str] = {"amount", "created_at", "status"}

class Transaction(BaseModel):
    id: int
    amount: float
    status: str
    tenant_id: str

def validate_and_sort_transactions(
    transactions: List[Transaction], 
    tenant_id: str, 
    sort_by: str
) -> List[Transaction]:
    # 1. Invariant: Input validation against whitelist
    if sort_by not in ALLOWED_SORT_COLUMNS:
        raise ValueError(f"Invalid sort parameter. Allowed: {ALLOWED_SORT_COLUMNS}")
    
    # 2. Invariant: Tenant Isolation
    tenant_txs = [tx for tx in transactions if tx.tenant_id == tenant_id]
    
    # 3. Secure Sort
    return sorted(tenant_txs, key=lambda x: getattr(x, sort_by), reverse=True)
