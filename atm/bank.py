class Bank:
    def __init__(self):
        self.accounts = {
            "card-bong": ["payroll_account", "nintendo_account"],
        }

        self.pins = {
           "card-bong": "1234",
        }

        self.balances = {
            "payroll_account": 500,
            "nintendo_account": 8000,
        }

    
    def validate_card(self, card_number):
        return card_number in self.accounts

    def validate_pin(self, card_number, pin):
        return self.pins.get(card_number) == pin
    
    def validate_account(self, card_number, account):
        return account in self.accounts.get(card_number, [])
    
    def get_accounts(self, card_number):
        return self.accounts.get(card_number, [])
    
    def get_account_balance(self, account):
        return self.balances.get(account, 0)
    
    
    def withdraw(self, account, amount):
        if account in self.balances and self.balances[account] >= amount:
            self.balances[account] -= amount
            return True
        return False
    
    def deposit(self, account, amount):
        if account in self.balances:
            self.balances[account] += amount
            return True
        return False
