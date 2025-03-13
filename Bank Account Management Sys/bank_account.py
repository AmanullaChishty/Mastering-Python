# Attributes:
# account_number: A unique identifier (you can auto-generate or let the user input).
# owner: Name of the account holder.
# balance: The current balance (should be a private attribute).

# Methods:
# deposit(amount): Increases the balance by the deposit amount.
# withdraw(amount): Decreases the balance by the specified amount if sufficient funds exist; otherwise, raise an exception.
# get_balance(): Returns the current balance.
# __str__(): Returns a user-friendly string representation of the account details.

import uuid


class BankAccount:
    total_accounts = 0

    def __init__(self,owner:str,initial_balance:float = 0.0):
        self.account_number = str(uuid.uuid4())
        self.owner = owner
        self.__balance = initial_balance
        BankAccount.total_accounts += 1
    
    def deposit(self,amount:float)-> None:
        if amount>0:
            self.__balance += amount
        else:
            print("Deposit must be positive. ")
    
    def withdraw(self, amount:float)->None:
        if amount>self.__balance:
            print("Insufficient Funds!")
        else:
            self.__balance-=amount
    
    def get_balance(self)->float:
        return self.__balance
    
    def __str__(self)->str:
        return f"Account[{self.account_number}] - Owner: {self.owner}, Balance: ${self.__balance:.2f}"
    
    @classmethod
    def get_total_accounts(cls)->int:
        return cls.total_accounts

    

