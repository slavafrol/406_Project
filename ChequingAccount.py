from __future__ import annotations
import BalanceAccount

class ChequingAccount(BalanceAccount.BalanceAccount):
    def __init__(self, balance: float=0):
        super().__init__(balance)
        self.type = "Chequing"

    def __str__(self):
        return f'Chequing account #{self.accountNumber} of {self.master.name_of_user}'