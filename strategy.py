class Strategy:
    #Schema for strategy representation, saved in .dat file

    #Important aspect of this is relative hand strength and tightness/aggressiveness factor

    #---bbbbb bbbbbbbb --pppppp ssssvvvv

    #b - bit turned on for for the value from ace to deuce
    #p - prime representation of the value, 2 for Deuce, up to 41 for Ace
    #s - suit of the card represented as a prime, 2-Clubs, 3-Spades, 5-Hearts, 7-Diamonds
    #v - value of the card starting with Deuce - 0, up to Ace - 12
    def __init__(self, strat):
        self.strat = strat