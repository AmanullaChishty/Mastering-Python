# SavingsAccount:
# Inherits from BankAccount.
# Has an additional attribute, e.g., interest_rate.
# Additional Methods:
# apply_interest(): Increases the balance based on the interest rate.

from bank_account import BankAccount

class SavingsAccount(BankAccount):
    def __init__(self, owner, initial_balance:float, interest_rate:float):
        super().__init__(owner, initial_balance)
        self.interest_rate = interest_rate
    
    def apply_interest(self)->None:
        interest = self.get_balance()*self.interest_rate
        self.deposit(interest)
    
    def __str__(self)->str:
        return f"Savings {super().__str__()}, Interest Rate: {self.interest_rate*100:.1f}%"