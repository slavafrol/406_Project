from __future__ import annotations
import UserAccount
import IDGenerator

class TellerAccount(UserAccount.UserAccount):
    def __init__(self, username: str, name: str, password: str):
        super().__init__(username, name, password=password)
        self.employeeID = IDGenerator.IDGenerator.generateEmployeeID()

    def __str__(self):
        return f" Username={self.username} \n Name={self.name_of_user} \n EmployeeID={self.employeeID} \n "