from enum import Enum, auto

class ATMState(Enum):
    NO_CARD = auto()
    CARD_INSERTED = auto()
    AUTHENTICATED = auto()
    ACCOUNT_SELECTED = auto()

class ATMController:
    def __init__(self, bank, cash_bin, max_pin_attempts=3):
        self.bank = bank
        self.cash_bin = cash_bin
        self.max_pin_attempts = max_pin_attempts
        self.pin_attempts = 0
        self.state = ATMState.NO_CARD
        self.current_card = None
        self.current_account = None


    def insert_card(self, card_number):
        if self.state == ATMState.NO_CARD:
            if self.bank.validate_card(card_number):
                self.current_card = card_number
                self.state = ATMState.CARD_INSERTED
                return True
        return False

    def enter_pin(self, pin):
        if self.state == ATMState.CARD_INSERTED:
            if self.bank.validate_pin(self.current_card, pin):
                self.state = ATMState.AUTHENTICATED
                self.pin_attempts = 0
                return True
            else:   
                self.pin_attempts += 1
                if self.pin_attempts >= self.max_pin_attempts:
                    self.eject_card()
                return False
        return False
    
    def select_account(self, account):
        if self.state == ATMState.AUTHENTICATED:
            if self.bank.validate_account(self.current_card, account):
                self.current_account = account
                self.state = ATMState.ACCOUNT_SELECTED
                return True
        return False
    
    def check_balance(self):
        if self.state == ATMState.ACCOUNT_SELECTED:
            return self.bank.get_account_balance(self.current_account)
        return None
    
    def deposit(self, amount):
        if self.state != ATMState.ACCOUNT_SELECTED:
            return False
        if amount <= 0:
            return False
        if self.bank.deposit(self.current_account, amount):
            self.cash_bin.add_cash(amount)
            return True
        return False
    
    def withdraw(self, amount):
        if self.state != ATMState.ACCOUNT_SELECTED:
            return False
        if amount <= 0:
            return False
        if not self.cash_bin.can_dispense(amount):
            return False
        if self.bank.withdraw(self.current_account, amount):
            self.cash_bin.dispense_cash(amount)
            return True
        return False

    def eject_card(self):
        self.state = ATMState.NO_CARD
        self.current_card = None
        self.current_account = None
        self.pin_attempts = 0   