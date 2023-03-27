from __future__ import annotations
import Transaction

class Etransfer(Transaction.Transaction):
    def __init__(self, amount: float, email: str=None, phone: str=None, sender: str="", receiver: str=""):
        super().__init__(amount, sender, receiver)
        self.email = email
        self.phone = phone

    def __str__(self):
        return f"Transaction ID: {self.transactionId}\nAmount: {self.amount}\nDate and Time: {self.dateTime}\n Email: {self.email} \n Phone Number: {self.phone}"
