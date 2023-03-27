from __future__ import annotations
import IDGenerator
import Transaction

class ATMWithdrawal(Transaction.Transaction):
    def __init__(self, amount: float, bank: str="T Bank", sender: str="", receiver: str=""):
        super().__init__(amount, sender, receiver)
        self.ATMID = IDGenerator.IDGenerator.generateAtmID()
        self.bank = bank