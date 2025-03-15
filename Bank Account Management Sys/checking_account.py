# CheckingAccount:
# Inherits from BankAccount.
# Implements a fee for each withdrawal.
# Overrides:
# The withdraw method to include a withdrawal fee deduction (make sure to check for sufficient funds after including the fee).

from bank_account import BankAccount
from custom_exceptions import InsufficientFundsError

class CheckingAccount(BankAccount):
    def __init__(self, owner:str, initial_balance:float,withdrawal_fee:float=1.0):
        super().__init__(owner, initial_balance)
        self.withdrawal_fee = withdrawal_fee
    
    def withdraw(self, amount:float) -> None:
        total_amount = amount + self.withdrawal_fee
        if total_amount>self.get_balance():
            raise InsufficientFundsError("Insufficient funds for withdrawal including fee.")
        super().withdraw(total_amount)
    
    def __str__(self) -> str:
        return f"Checking {super().__str__()}, Withdrawal Fee: ${self.withdrawal_fee:.2f}"