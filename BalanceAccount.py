from __future__ import annotations
import datetime
import UserAccount
import Transaction
import SelfTransaction
import AutoPayment
import WireTransfer
import Payee
import Etransfer
import EtransferPayee
import ClientAccount
import Purchase
import ATMWithdrawal
import Card
import main
import IDGenerator

class BalanceAccount:
    def __init__(self, master: ClientAccount.ClientAccount, balance: float, paymentNetwork: str="Visa"):
        self.master = master
        self.accountNumber = IDGenerator.IDGenerator.generateBalanceAccountID()
        self.balance = balance
        self.card = Card.Card(paymentNetwork=paymentNetwork)
        self.transactions = []
        self.autoPayments = []
        self.observers = [master] #add the client account of this balance account to observe by default
        self.notifOnAmount = None
        self.creationDate = datetime.date.today()

    def addObserver(self, observer):
        self.observers.append(observer)
    
    def removeObserver(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def notifyObservers(self, notification: str):
        for obs in self.observers:
            if obs.isinstance(UserAccount.UserAccount):
                obs.update(notification)

    def setNotifAmount(self, amount):
        self.notifOnAmount = amount

    def deposit(self, amount: float):
        self.balance = self.balance + amount

    #do not use this method directly!
    def withdraw(self, amount: float):
        if amount > self.balance:
            return False
        if self.notifAmount and amount > self.notif:
            notification = f'A transaction for amount {amount}CAD has been performed on balance account #{self.accountNumber} of client account #{self.master.getAccountNumber()}'
            self.notifyObservers(notification)
        self.balance -= amount

    #do not use directly
    def newTransaction(self, transaction: Transaction.Transaction):
        self.transactions.append(transaction)

    def transferBetweenAccounts(self, amount: float, account2: 'BalanceAccount'):
        if amount > self.balance:
            return False
        transfer = SelfTransaction.SelfTransaction(amount, str(self), str(account2))
        self.newTransaction(transfer)

        self.withdraw(amount)
        self.newTransaction(transfer)

        account2.deposit(amount)
        account2.newTransaction(transfer)


    def setupAutoPayment(self, payee: Payee.Payee, amount: float, freq: datetime.timedelta=datetime.timedelta(days=30)):
        autoPayment = AutoPayment.AutoPayment(payee, freq, amount)
        self.autoPayments.append(autoPayment)


    def sendWireTransfer(self, amount: float, details: str):
        if amount > self.balance:
            return False
        wire = WireTransfer.WireTransfer(amount, details, str(self))
        self.withdraw(amount)
        self.newTransaction(wire)
        return True
    
    
    def sendEtransfer(self, amount: float, email: str=None, phone: str=None):
        if amount > self.balance:
            return False
        if email and phone:
            for payee in self.master.payees:
                if payee.isinstance(EtransferPayee.EtransferPayee) and payee.email == email and payee.phone == phone:
                    for account in main.AccountInterface.clientAcc: #check if in the same bank
                        if account.phone == phone and account.email == email:
                            etransfer = Etransfer.Etransfer(amount, email, phone, str(self), str(account))
                            self.withdraw(amount)
                            self.newTransaction(etransfer)
                            account.newTransaction(etransfer)
                            account.deposit(amount)
                            return True
                    etransfer = Etransfer.Etransfer(amount, email, phone, str(self), email)
                    self.withdraw(amount)
                    self.newTransaction(etransfer)
                    return True
            return False #payee not found in self.payees
        elif email:
            for payee in self.master.payees:
                if payee.isinstance(EtransferPayee.EtransferPayee) and payee.email == email:
                    for account in main.AccountInterface.clientAcc:
                        if account.email == email:
                            etransfer = Etransfer.Etransfer(amount, email, sender=str(self), receiver=str(account))
                            self.withdraw(amount)
                            self.newTransaction(etransfer)
                            account.newTransaction(etransfer)
                            account.deposit(amount)
                            return True
                        etransfer = Etransfer.Etransfer(amount, email, sender=str(self), receiver=email)
                        self.withdraw(amount)
                        self.newTransaction(etransfer)
                return True
            return False
        elif phone:
            for payee in self.master.payees:
                if payee.isinstance(EtransferPayee.EtransferPayee) and payee.phone == phone:
                    for account in main.AccountInterface.clientAcc:
                        if account.phone == phone:
                            etransfer = Etransfer.Etransfer(amount, phone=phone, sender=str(self), receiver=str(account))
                            self.withdraw(amount)
                            self.newTransaction(etransfer)
                            account.newTransaction(etransfer)
                            account.deposit(amount)
                            return True
                    etransfer = Etransfer.Etransfer(amount, phone=phone, sender=str(self), receiver=phone)
                    self.withdraw(amount)
                    self.newTransaction(etransfer)
                    return True
        return False
    

    def makePurchase(self, amount: float, name: str, location: str):
        if amount > self.balance:
            return False
        purchase = Purchase.Purchase(amount, name, location, str(self))
        self.withdraw(amount)
        self.newTransaction(purchase)
        return True
    
    def withdrawATM(self, amount: float, bank: str="T Bank"):
        if amount > self.balance:
            return False
        atmwithdrawal = ATMWithdrawal.ATMWithdrawal(amount, bank, str(self), bank)
        self.withdraw(amount)
        self.newTransaction(atmwithdrawal)
        return True