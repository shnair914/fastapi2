import pytest
from app.calculations import subtract, divide, BankAccount

@pytest.fixture
def zero_bank_balance():
    return BankAccount()

@pytest.fixture
def bank_account_with_balance():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 1),
    (7, 1, 6),
    (8, 4, 4) 
])
def test_subtract(num1, num2, expected):
    assert subtract(num1, num2) == expected

def test_divide():
    assert divide(2, 2) == 1

def test_bank_initial_amount():
    bank_account = BankAccount(50)
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_balance):
    assert zero_bank_balance.balance == 0

def test_withdraw():
    new_bc = BankAccount(100)
    new_bc.withdraw(60)
    assert new_bc.balance == 40

def test_bank_transaction(zero_bank_balance):
    zero_bank_balance.deposit(200)
    zero_bank_balance.withdraw(60)
    assert zero_bank_balance.balance == 140

