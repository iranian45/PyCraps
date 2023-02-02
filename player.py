from chips import *
from crapstable import *

table = CrapsTable(screen)

class Player:
    def __init__(self):
        self.chips = Chips(self)
        self.bankroll = 500
        self.bet_amount = 0

    def place_bet(self, bet_amount):
        pass
        
    
      