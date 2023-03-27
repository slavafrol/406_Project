from __future__ import annotations
import datetime
import Payee

class AutoPayment:
    def __init__(self, payee: Payee.Payee, paymentRate: datetime.timedelta, amount: int):
        self.payee = payee
        self.paymentRate = paymentRate
        self.amount = amount

    def changeAmount(self, newAmount: int):
        self.amount = newAmount

    def changeRate(self, newRate: datetime.timedelta):
        self.paymentRate = newRate