class CashBin:
    def __init__(self, initial_cash=0):
        self.cash = initial_cash

    def add_cash(self, amount):
        self.cash += amount

    def get_cash(self):
        return self.cash
    
    def can_dispense(self, amount):
        return self.cash >= amount
    
    def dispense_cash(self, amount):
        if self.can_dispense(amount):
            self.cash -= amount
            return True
        return False   
    
