from __future__ import annotations
import datetime
import UserAccount
import BalanceAccount
import ChequingAccount
import SavingsAccount
import CreditAccount
import Etransfer
import Loan
import Payee
import main

class ClientAccount(UserAccount.UserAccount):
    def __init__(self, username: str, name: str, accountNumber: int, password: str, email: str, phone: str, address: str):
        super().__init__(username, name, accountNumber, password)
        self.e_mail = email
        self.phone_no = phone
        self.address = address
        self.loans = []
        self.payees = []
        self.incomingRequests = []
        self.incomingEtransfers = []
        self.chequingAccount = ChequingAccount.ChequingAccount(self)
        self.savingsAccounts = []
        self.creditAccounts = []
        self.balanceAccounts = [self.chequingAccount] + self.savingsAccounts + self.creditAccounts

    def changeEmail(self, newEmail: str):
        self.e_mail = newEmail
        return True

    def changePhone(self, newPhone: str):
        self.phone_no = newPhone

    def changeAddress(self, newAddr: str):
        self.address = newAddr
        return True

    def applyLoan(self, amount: float, type: Loan.Loan, startDate: datetime.datetime, endDate: datetime.datetime):
        loan = Loan.Loan(amount, type, startDate, endDate)
        self.loans.append(loan)

    def addPayee(self, payee: Payee.Payee):
        self.payees.append(payee)

    def openCreditAccount(self, balance: float):
        credit = CreditAccount.CreditAccount(self)
        self.creditAccounts.append(credit)
        return True

    def openSavingsAccount(self):
        savings = SavingsAccount.SavingsAccount(self)
        self.savingsAccounts.append(savings)
        return True
    
    def acceptEtransfer(self, etransfer: Etransfer.Etransfer):
        if etransfer in self.incomingEtransfers:
            self.incomingEtransfers.remove(etransfer)
            self.chequingAccount.deposit(etransfer.amount)
            return True
        return False
    
    def requestMoney(self, amount, requestee):
        if requestee in main.AccountInterface.clientAcc:
            main.AccountInterface.clientAcc.incomingRequests.append((self, amount))
            return True
        return False #if client does not exist
    
    def fulfillRequest(self, request):
        requester, amount = request
        if self.chequingAccount.balance > amount:
            return False #not enough funds
        self.chequingAccount.balance -= amount
        requester.chequingAccount.balance += amount
        self.incomingRequests.remove(request)
        return True
    
    def cancelBalanceAccount(self, account: BalanceAccount.BalanceAccount):
        if account in self.balanceAccounts:
            self.balanceAccounts.remove(account)
            return True
        return False #balance account does not exist
    
    def makeLoanPayment(self, account: BalanceAccount.BalanceAccount, amount: int, loan: Loan.Loan):
       if amount > account.balance:
           return False
       account.withdraw(amount)
       loan.pay(amount)
       return True

    def __str__(self):
        return f"ClientAccount(username={self.username}, name={self.name_of_user}, password = {self._password}, email={self.e_mail}, phone={self.phone_no}, address={self.address}, loans={self.loans}, payees={self.payees}, incomingEtransfers={self.incomingEtransfers}, balanceAccount={self.balanceAccount})"