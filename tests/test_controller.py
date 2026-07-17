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


def test_deposit_valid_amount():
    bank = Bank()
    cash_bin = CashBin()
    atm = ATMController(bank, cash_bin)
    atm.insert_card("card-bong")
    atm.enter_pin("1234")
    atm.select_account("payroll_account")
    result = atm.deposit(100)

    assert result
    assert bank.get_account_balance("payroll_account") == 600
    assert cash_bin.get_cash() == 100


def test_deposit_invalid_amount():
    bank = Bank()
    cash_bin = CashBin()
    atm = ATMController(bank, cash_bin)
    atm.insert_card("card-bong")
    atm.enter_pin("1234")
    atm.select_account("payroll_account")
    result = atm.deposit(0)

    assert not result
    assert bank.get_account_balance("payroll_account") == 500
    assert cash_bin.get_cash() == 0


def test_withdraw_valid_amount():
    bank = Bank()
    cash_bin = CashBin(initial_cash=1000)
    atm = ATMController(bank, cash_bin)
    atm.insert_card("card-bong")
    atm.enter_pin("1234")
    atm.select_account("payroll_account")
    result = atm.withdraw(500)

    assert result
    assert bank.get_account_balance("payroll_account") == 0
    assert cash_bin.get_cash() == 500


def test_withdraw_invalid_amount():
    bank = Bank()
    cash_bin = CashBin(initial_cash=2000)
    atm = ATMController(bank, cash_bin)
    atm.insert_card("card-bong")
    atm.enter_pin("1234")
    atm.select_account("payroll_account")
    result = atm.withdraw(1500)

    assert not result
    assert bank.get_account_balance("payroll_account") == 500
    assert cash_bin.get_cash() == 2000


def test_withdraw_over_cash_bin_limit():
    bank = Bank()
    cash_bin = CashBin(initial_cash=500)
    atm = ATMController(bank, cash_bin)
    atm.insert_card("card-bong")
    atm.enter_pin("1234")
    atm.select_account("nintendo_account")
    result = atm.withdraw(2500)

    assert not result
    assert bank.get_account_balance("nintendo_account") == 8000
    assert cash_bin.get_cash() == 500


def test_withdraw_before_account_selected():
    bank = Bank()
    cash_bin = CashBin(initial_cash=1000)
    atm = ATMController(bank, cash_bin)
    atm.insert_card("card-bong")
    atm.enter_pin("1234")
    result = atm.withdraw(500)

    assert not result


def test_eject_card_resets_state():
    bank = Bank()
    cash_bin = CashBin()
    atm = ATMController(bank, cash_bin)
    atm.insert_card("card-bong")
    atm.enter_pin("1234")
    atm.select_account("nintendo_account")
    atm.eject_card()

    assert atm.state == ATMState.NO_CARD
    assert atm.current_card is None
    assert atm.current_account is None

def test_withdraw_towards_nintendo():
    bank = Bank()
    cash_bin = CashBin(initial_cash=10000)
    atm = ATMController(bank, cash_bin)

    assert atm.insert_card("card-bong")
    assert atm.enter_pin("1234")
    assert atm.select_account("nintendo_account")
    assert atm.withdraw(7000)
    assert bank.get_account_balance("nintendo_account") == 1000
    assert cash_bin.get_cash() == 3000