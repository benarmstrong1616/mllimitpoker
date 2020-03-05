import random
from bot import Bot
from player import Player

class Game:
    def __init__(self, solo, bots, hands=-1):
        self.solo = solo
        self.hands = hands
        if solo:
            self.p1 = Player()
            self.p2 = bots[0]
        else:
            self.p1 = bots[0]
            self.p2 = bots[1]
        self.deck = ['ac', 'as', 'ah', 'ad', 'kc', 'ks', 'kh', 'kd',
                     'qc', 'qs', 'qh', 'qd', 'jc', 'js', 'jh', 'jd',
                     '10c', '10s', '10h', '10d', '9c', '9s', '9h', '9d',
                     '8c', '8s', '8h', '8d', '7c', '7s', '7h', '7d',
                     '6c', '6s', '6h', '6d', '5c', '5s', '5h', '5d',
                     '4c', '4s', '4h', '4d', '3c', '3s', '3h', '3d',
                     '2h', '2d', '2h', '2d']

    def begin(self):
        current_totals = [0,0]
        random.shuffle(self.deck)
        resume = True
        self.hand_count = 0
        while(resume):
            self.hand_count = self.hand_count + 1
            print("Hand Number " + str(self.hand_count))
            print("Shuffle up and deal...")
            hand_res = self.play_hand()
            current_totals[0] = current_totals[0] + hand_res[0]
            current_totals[1] = current_totals[1] + hand_res[1]
            if current_totals[0] > -1 :
                print("Player 1 is up " + str(current_totals[0]))
            else:
                print("Player 1 is down " + str(current_totals[0]))
            if current_totals[1] > -1 :
                print("Player 2 is up " + str(current_totals[0]))
            else:
                print("Player 2 is down " + str(current_totals[0]))
            resume = hand_res[2]

    def play_hand(self):
        result = [0,0,True]
        if (self.hand_count % 2) == 0:
            current_p1 = self.p1
            current_p2 = self.p2
            p1_index = 0
            p2_index = 1
        else:
            current_p1 = self.p2
            current_p2 = self.p1
            p1_index = 1
            p2_index = 0
        p1_stack = 500
        p2_stack = 500
        pot = 0
        print("PREFLOP ACTION")
        p1_stack = p1_stack - 10
        p2_stack = p2_stack - 5
        pot = pot + 15
        p2_pf_dec = current_p2.make_decision(p2_stack, pot, [self.deck[2],self.deck[3]], [], ['c','r','f'])
        if p2_pf_dec == 'f':
            p1_stack = p1_stack + pot
        elif p2_pf_dec == 'c':
            p2_stack = p2_stack - 5
            pot = pot + 5
            p1_pf_dec = current_p1.make_decision(p1_stack, pot, [self.deck[0],self.deck[1]], [], ['x','r'])
            if p1_pf_dec == 'r':
                p1_stack = p1_stack - 10
                pot = pot + 10
                p2_pf_dec = current_p2.make_decision(p2_stack, pot, [self.deck[2],self.deck[3]], [], ['c', 'f'])
                if p2_pf_dec == 'c':
                    p2_stack = p2_stack - 10
                    pot = pot + 10
                else:

        if self.solo:
            result[2] = self.p1.resume()
        else:
            result[2] = not (self.hand_count == self.hands)
        return result




