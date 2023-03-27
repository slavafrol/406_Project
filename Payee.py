from __future__ import annotations
import IDGenerator

class Payee:
    def __init__(self, name: str, description: str):
        self.payeeID = IDGenerator.IDGenerator.generatePayeeID()
        self.name = name
        self.description = description

    def change_name(self, name: str):
        self.name = name

    def change_payeeID(self, id: int):
        self.payeeID = id

    def change_description(self, descp: str):
        self.description = descp

    def __str__(self):
        return f"Payee ID #{self.payeeID}, {self.name}"