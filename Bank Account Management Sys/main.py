from saving_account import SavingsAccount
from checking_account import CheckingAccount
from custom_exceptions import InsufficientFundsError
from bank_account import BankAccount

def main():
    savings = SavingsAccount("Alice",1000,0.03)
    checking = CheckingAccount("Bob",500,2.0)

    print(savings)
    savings.deposit(200)
    savings.apply_interest()
    print(savings)

    print(checking)

    try:
        checking.withdraw(100)
    except InsufficientFundsError as e:
        print("Withdrawal failed:",e)
    print(checking)

    print(f"Total accounts created: {BankAccount.get_total_accounts()}")

if __name__=="__main__":
    main()
