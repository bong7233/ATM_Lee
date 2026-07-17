class Bank:
    def __init__(self):
        self.accounts = {
            "card-bong": ["account1", "account2"],
        }

        self.pins = {
           "card-bong": "1234",
        }

        self.balances = {
            "account1": 1000,
            "account2": 500,
        }

    
    def validate_card(self, card_number):
        return card_number in self.accounts

    def validate_pin(self, card_number, pin):
        return self.pins.get(card_number) == pin
    
    
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
