class Dealer:
    def __init__(self, min_bet, max_bet):
        self.min_bet = min_bet
        self.max_bet = max_bet

    def set_table_limits(self, min_bet, max_bet):
        self.min_bet = min_bet
        self.max_bet = max_bet
        
    def check_bet(self,bet):
        if bet<self.min_bet:
            print("Bet is below the minimum limit of ",self.min_bet)
            return False
        elif bet>self.max_bet:
            print("Bet is above the maximum limit of ",self.max_bet)
            return False
        else:
            return True