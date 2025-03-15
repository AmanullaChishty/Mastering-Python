class InsufficientFundsError(Exception):
    """Exception raised when a withdrawal amount exceeds the available balance"""
    pass