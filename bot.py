from strategy import Strategy
import random
from evaluator import evaluate, percentile, board_texture, hand_strength
from operator import itemgetter

class Bot:
    def __init__(self, strat=None, load=False):
        #initialise the strategy with the file name and whether to load or create a fresh file
        self.strategy = Strategy(strat, load)
        #simple dict to convert between char and int value for decisions
        self.opt_dict = {'f':0,'x':1,'c':2,'b':3,'r':4}
        #initialise current hand
        self.current_hand = []

    def make_decision(self, pot, current_bet, hand, board, options):
        opts = []
        for o in options:
            #all valid options
            opts.append(self.opt_dict[o])
        #use evaluator functions to work out current scenario for regrets
        value = evaluate(hand+board)
        tex = board_texture(board)
        strength = hand_strength(value)
        perc = percentile(hand,board,value)
        round_idx = len(board) - 3
        #access regrets that match the current scenario
        regrets = self.strategy.get_regrets(tex,strength,perc,round_idx,opts)
        if len(regrets) > 1:
            #Use size of the pot and where we are in the hand
            #to see how important the decision is and how much weight to put on regrets
            sorted_regrets = sorted(regrets, key=itemgetter(1), reverse=True)
            if (sorted_regrets[0][1] - sorted_regrets[1][1]) > (len(board)*pot):
            	r_opt = sorted_regrets[0][0]
            else:
            	#Randomly choose between best 2 options
                r_opt = sorted_regrets[random.randint(0,1)][0]
            dec = list(self.opt_dict.keys())[list(self.opt_dict.values()).index(r_opt)]
            #add decision made to current hand for storing regret later in hand
            self.current_hand.append([tex,strength,perc,round_idx,r_opt])
        else:
            #if no regrets are available for current scenario then randomly choose
            random.shuffle(options)
            dec = self.opt_dict[options[0]]
            #add decision made to current hand for storing regret later in hand
            self.current_hand.append([tex,strength,perc,round_idx,dec])
            dec = options[0]
        return dec


    def make_preflop_decision(self, pot, raise_made, hand, options, dealer):
        #preflop currently random as not important stage in the hand
        random.shuffle(options)
        return options[0]

    def update_strategy(self, result):
        #store the regret based on result of current hand
        for h in self.current_hand:
            self.strategy.update_regret(h[0],h[1],h[2],h[3],h[4],result)
        #clear hand once regret has been stored to prepare for the next hand
        self.current_hand = []

    def save_strategy(self):
        #save strategy to file
        self.strategy.save_strategy()

