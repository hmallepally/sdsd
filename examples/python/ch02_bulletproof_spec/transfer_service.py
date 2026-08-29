import asyncio
from decimal import Decimal
from typing import Dict

class BankLedger:
    def __init__(self):
        self.accounts: Dict[str, Decimal] = {}
        self.lock = asyncio.Lock()

    def set_balance(self, account_id: str, amount: Decimal):
        self.accounts[account_id] = amount

    def get_total_balance(self) -> Decimal:
        return sum(self.accounts.values(), Decimal("0.00"))

    async def transfer(self, from_acc: str, to_acc: str, amount: Decimal) -> bool:
        # Atomic lock ensuring Conservation of Mass
        async with self.lock:
            if self.accounts.get(from_acc, Decimal("0")) < amount:
                return False
            self.accounts[from_acc] -= amount
            self.accounts[to_acc] += amount
            return True
