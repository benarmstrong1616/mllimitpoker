from strategy import Strategy
import random

class Bot:
    def __init__(self, strat):
        if strat in ['1','2','3','4']:
            self.strat = Strategy(int(strat))
        else:
            self.strat = Strategy(random.randint(1,5))

    def make_decision(self, pot, current_bet, hand, board, options):
        random.shuffle(options)
        return options[0]

    def make_preflop_decision(self, pot, raise_made, hand, options, dealer):
        random.shuffle(options)
        return options[0]
