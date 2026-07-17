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

def test_enter_invalid_pin_max_attempts():
    bank = Bank()
    cash_bin = CashBin()
    atm = ATMController(bank, cash_bin)
    atm.insert_card("card-bong")

    for _ in range(atm.max_pin_attempts):
        atm.enter_pin("7777")

    assert atm.state == ATMState.NO_CARD