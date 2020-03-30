from strategy import Strategy
import random
from evaluator import evaluate, percentile, board_texture, hand_strength
from operator import itemgetter

class Bot:
    def __init__(self, strat=None):
        self.strategy = Strategy(strat)
        self.opt_dict = {'f':0,'x':1,'c':2,'b':3,'r':4}
        self.current_hand = []

    def make_decision(self, pot, current_bet, hand, board, options):
        opts = []
        for o in options
            opts.append(self.opt_dict[o])
        value = evaluate(hand.extend(board))
        tex = board_texture(board)
        strength = hand_strength(value)
        perc = percentile(hand,board,value)
        round_idx = len(board) - 3
        regrets = self.strategy.get_regrets(tex,strength,perc,round_idx,opts)
        if regrets:
            regret_sum = 0
            for a, b in regrets:
                regret_sum += abs(b)
            regret_probs = []
            sum_probs = 0
            for a,b in regrets:
                sum_probs += (b/regret_sum + 1)/2
                regret_probs.append(a,sum_probs)
            regret_probs = sorted(regret_probs,key=itemgetter(1))
            decision_prob = random.randint(1,100000) / 100000
            for a,b in regret_probs:
                if decision_prob <= b:
                	dec = list(opts.keys())[list(opts.values()).index(a)]
                	self.current_hand.append([tex,strength,perc,round_idx,dec])
                    return dec
        else:
            random.shuffle(options)
            self.current_hand.append([tex,strength,perc,round_idx,options[0]])
            return options[0]


    def make_preflop_decision(self, pot, raise_made, hand, options, dealer):
        random.shuffle(options)
        return options[0]
