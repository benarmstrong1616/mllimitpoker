import pickle
import copy

class Strategy:
    #Schema for strategy representation, saved in .dat file

    #Important aspect of this is board texture against current hand to find tightness/aggressiveness factor

    #Board Texture values:
    #0 - Unique Rainbow
    #1 - 3 to a Flush
    #2 - 4 to a Straight
    #3 - Paired
    #4 - 3 to a Flush + Paired
    #5 - 4 to a Flush
    #6 - Double Paired
    #7 - Trips

    #Rank values:
    #0 - High Card
    #1 - One Pair
    #2 - Two Pairs
    #3 - Three of a kind
    #4 - Straight
    #5 - Flush
    #6 - Full House
    #7 - Four of a kind
    #8 - Straight Flush

    #Rank Percentiles - will be rounded down to nearest 0.05
    #0 - 0.00
    #1 - 0.05
    #...
    #18 - 0.90
    #19 - 0.95

    #Round - Flop, Turn or River (preflop handled separately)
    #0 - Flop
    #1 - Turn
    #2 - River

    #Decision
    #0 - Fold
    #1 - Check
    #2 - Call
    #3 - Bet
    #4 - Raise
    def __init__(self, strat_file=None, load=True):
        self.textures = 8
        self.ranks = 9
        self.percentiles = 20
        self.rounds = 3
        self.decisions = 5
        self.strategy = None
        self.strat_file = strat_file
        if strat_file and load:
            self.strat_file = strat_file
            pickle_file = open(self.strat_file, 'rb')
            self.strategy = copy.deepcopy(pickle.load(pickle_file))
        if not self.strategy:
        	self.strategy = self.initialise_strategy()

    def initialise_strategy(self):
        #create an empty 5-dimensional array with None values
        a = [ [ [ [ [ None for i in range(self.decisions) ] for j in range(self.rounds) ] for k in range(self.percentiles) ] for l in range(self.ranks) ] for m in range(self.textures) ]
        return a

    def update_regret(self, texture, rank, percentile, round_idx, dec, regret):
        if self.strategy[texture][rank][percentile][round_idx][dec]:
            self.strategy[texture][rank][percentile][round_idx][dec] += regret
        else:
            self.strategy[texture][rank][percentile][round_idx][dec] = regret

    def get_regrets(self, texture, rank, percentile, round_idx, possible_decs):
        action_point = self.strategy[texture][rank][percentile][round_idx]
        regrets = []
        if action_point:
            for idx in possible_decs:
                if action_point[idx]:
                    regrets.append((idx,action_point[idx]))
        return regrets

    def save_strategy(self):
        #saving array to the pickle file
        output = open(self.strat_file, 'wb')
        pickle.dump(self.strategy, output)
        #closing file after use to save system memory
        output.close()
