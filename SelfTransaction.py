from __future__ import annotations
import Transaction

class SelfTransaction(Transaction.Transaction):
    def __init__(amount: float, sender: str="", receiver: str=""):
        super().__init__(amount, sender, receiver)