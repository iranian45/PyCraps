from chips import *
from crapstable import *


class Player:
    def __init__(self):
        self.table = CrapsTable(screen)
        self.chips = Chips(self)
        self.bankroll = 500
        self.bet_amount = 0

    def handle_betting(self, pos):          
            for point, rect in self.table.point_rect_dict.items():
                if rect.collidepoint(pos):
                    if self.chips.selected_chip:
                        self.bet_amount += self.chips.selected_chip
                        self.bankroll -= self.chips.selected_chip
                        
                    print(f"bet amount is {self.bet_amount}")
                    print(f"new bankroll is {self.bankroll}")    
                    print(self.chips.selected_chip) 
                    print(point)
                    return point, self.bet_amount, self.bankroll, self.chips.selected_chip
            return None
    

    #3492018734091823