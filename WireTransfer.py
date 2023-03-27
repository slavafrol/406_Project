from __future__ import annotations
import Transaction

class WireTransfer(Transaction.Transaction):
    def __init__(self, amount: float, details: str, sender: str=""):
        super().__init__(amount, sender, details)
        self.details = details

    def __str__(self):
        return f"Transaction ID: {self.transactionId}\nAmount: {self.amount}\nDate and Time: {self.dateTime}\n Details: {self.details}"