from atm.bank import Bank
from atm.cash_bin import CashBin
from atm.controller import ATMController, ATMState


def test_insert_valid_card():
    bank = Bank()
    cash_bin = CashBin()
    atm = ATMController(bank, cash_bin)
    result = atm.insert_card("card-bong")

    assert result
    assert atm.state == ATMState.CARD_INSERTED


def test_insert_invalid_card():
    bank = Bank()
    cash_bin = CashBin()
    atm = ATMController(bank, cash_bin)
    result = atm.insert_card("card-bear")

    assert not result
    assert atm.state == ATMState.NO_CARD

def test_enter_valid_pin():
    bank = Bank()
    cash_bin = CashBin()
    atm = ATMController(bank, cash_bin)
    atm.insert_card("card-bong")
    result = atm.enter_pin("1234")

    assert result
    assert atm.state == ATMState.AUTHENTICATED

def test_enter_invalid_pin_less_than_max_attempts():
    bank = Bank()
    cash_bin = CashBin()
    atm = ATMController(bank, cash_bin)
    atm.insert_card("card-bong")

    for _ in range(atm.max_pin_attempts - 1):
        atm.enter_pin("7777")    
    
    assert atm.state == ATMState.CARD_INSERTED


def test_enter_invalid_pin_max_attempts():
    bank = Bank()
    cash_bin = CashBin()
    atm = ATMController(bank, cash_bin)
    atm.insert_card("card-bong")

    for _ in range(atm.max_pin_attempts):
        atm.enter_pin("7777")

    assert atm.state == ATMState.NO_CARD


def test_select_valid_account():
    bank = Bank()
    cash_bin = CashBin()
    atm = ATMController(bank, cash_bin)
    atm.insert_card("card-bong")
    atm.enter_pin("1234")
    result = atm.select_account("payroll_account")

    assert result
    assert atm.state == ATMState.ACCOUNT_SELECTED

def test_select_invalid_account():
    bank = Bank()
    cash_bin = CashBin()
    atm = ATMController(bank, cash_bin)
    atm.insert_card("card-bong")
    atm.enter_pin("1234")
    result = atm.select_account("Cartier_account")

    assert not result
    assert atm.state == ATMState.AUTHENTICATED


def test_check_balance():
    bank = Bank()
    cash_bin = CashBin()
    atm = ATMController(bank, cash_bin)
    atm.insert_card("card-bong")
    atm.enter_pin("1234")
    atm.select_account("payroll_account")
    balance = atm.check_balance()

    assert balance == 500
    assert atm.state == ATMState.ACCOUNT_SELECTED 

def test_check_balance_without_account_selected():
    bank = Bank()
    cash_bin = CashBin()
    atm = ATMController(bank, cash_bin)
    atm.insert_card("card-bong")
    atm.enter_pin("1234")

    assert atm.check_balance() is None


