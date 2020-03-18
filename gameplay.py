from bot import Bot
from player import Player
from datetime import datetime
from evaluator import evaluate
import random
import copy

class Game:
    def __init__(self, player=False, history_file="handhistory.txt"):
        self.players = [None, None]
        self.player = player
        if player:
            self.players[0] = Player()
        else:
            self.players[0] = Bot(1)
        self.players[1] = Bot(1)
        self.deck = ['ac', 'as', 'ah', 'ad', 'kc', 'ks', 'kh', 'kd',
                     'qc', 'qs', 'qh', 'qd', 'jc', 'js', 'jh', 'jd',
                     '10c', '10s', '10h', '10d', '9c', '9s', '9h', '9d',
                     '8c', '8s', '8h', '8d', '7c', '7s', '7h', '7d',
                     '6c', '6s', '6h', '6d', '5c', '5s', '5h', '5d',
                     '4c', '4s', '4h', '4d', '3c', '3s', '3h', '3d',
                     '2h', '2d', '2c', '2s']
        self.blinds = [1,2]
        self.history_file = history_file
        self.counts = (0,0)

    def start(self, hands=20):
        hist_file = open(self.history_file, "a")
        hist_file.write("{0}\n".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
        for x in range(hands):
            hist_file.write("Hand{0}\n".format(x+1))
            if self.player:
                print("\nHand{0}\n".format(x+1))
            hand_res = self.play_hand(x%2)
            if x%2 == 1:
                num_res = [hand_res[1], hand_res[0]]
            else:
                num_res = [hand_res[0], hand_res[1]]
            self.counts = (self.counts[0]+num_res[0], self.counts[1]+num_res[1])
            hist_file.write(hand_res[2])
            hist_file.write("\nUpdated Counts: {0}, {1}\n".format(self.counts[0], self.counts[1]))
        if self.counts[0] > self.counts[1]:
            winner = "Player1"
        elif self.counts[1] > self.counts[0]:
            winner = "Player2"
        else:
            winner = "nobody"
        hist_file.write("End of session, {0} wins".format(winner))
        hist_file.close()

    def play_hand(self, dealer=0):
        random.shuffle(self.deck)
        cur_dealer = self.players[dealer]
        cur_opp = self.players[1-dealer]
        dealer_hc = [self.deck[0], self.deck[1]]
        opp_hc = [self.deck[2], self.deck[3]]
        boardcards = [self.deck[4], self.deck[5], self.deck[6], self.deck[8], self.deck[10]]
        final_result = None
        hand_string = ""
        final_pot = 0
        rounds = ["PREFLOP", "FLOP", "TURN", "RIVER"]
        line = "-"*10
        for x in range(4):
            if self.player:
                print(line,rounds[x],line)
            if x == 0:
                result = self.play_preflop(cur_dealer, cur_opp, dealer_hc, opp_hc, 3)
                hand_string = result[2]
            else:
                result = self.play_round(cur_dealer, cur_opp, dealer_hc, opp_hc, boardcards[0:(2+x)], result[0])
                hand_string += "\n{0}".format(result[2])
            if result[1]:
                final_result = result[1]
                break
            final_pot = result[0]
        if final_result:
            final_result.append(hand_string)
            return final_result
        else:
            showdown_res = self.showdown(dealer_hc, opp_hc, boardcards, final_pot, hand_string)
            return showdown_res

    def play_round(self, p1, p2, p1hc, p2hc, bc, pot):
        cur_pot = pot
        invested = [-(pot/2), -(pot/2)]
        raises_made = 0
        players = [p2, p1]
        hcs = [p2hc, p1hc]
        names = ["BB", "Dealer"]
        move_count = 0
        info_string = ""
        next_p_options = ['x', 'b']
        options_after_raise = [['f', 'c', 'r'], ['f', 'c']]
        raise_or_bet = ["bets", "raises to"]
        cur_bet = 0
        while True:
            player_idx = move_count%2
            dec = players[player_idx].make_decision(cur_pot, cur_bet, hcs[player_idx], bc, next_p_options)
            if dec == 'f':
                info_string += "{0} folds, {1} wins pot of {2}".format(names[player_idx], names[1-player_idx], cur_pot)
                if self.player:
                    print("{0} folds, {1} wins pot of {2}".format(names[player_idx], names[1-player_idx], cur_pot))
                invested[player_idx] += cur_pot
                return [cur_pot, invested, info_string]
            elif dec == 'x':
                info_string += "{0} checks ".format(names[player_idx])
                if self.player:
                    print("{0} checks ".format(names[player_idx]))
                if move_count != 0:
                    return [cur_pot, None, info_string]
            elif dec == 'c':
                info_string += "{0} calls ".format(names[player_idx])
                if self.player:
                    print("{0} calls ".format(names[player_idx]))
                if raises_made == 1:
                    cur_pot = pot*2
                else:
                    cur_pot = pot*3
                return [cur_pot, None, info_string]
            else:
                cur_bet = pot/2
                if raises_made == 1:
                    cur_bet = cur_bet*2
                info_string += "{0} {1} {2} ".format(names[player_idx], raise_or_bet[raises_made], cur_bet)
                if self.player:
                    print("{0} {1} {2} ".format(names[player_idx], raise_or_bet[raises_made], cur_bet))
                next_p_options = options_after_raise[raises_made]
                raises_made += 1
                invested[1-player_idx] -= ((pot/2)*raises_made)
                cur_pot += ((pot/2)*raises_made)
            move_count += 1

    def play_preflop(self, p1, p2, p1hc, p2hc, pot):
        info_string = ""
        cur_pot = pot
        p1_invested = -1
        p2_invested = -2
        dealer_dec = p1.make_preflop_decision(cur_pot, False, p1hc, ['f', 'c', 'r'], True)
        if dealer_dec == 'f':
            info_string += "Dealer folds, BB wins pot of {0}".format(cur_pot)
            if self.player:
                print(info_string)
            return [cur_pot, [p1_invested, p2_invested+cur_pot], info_string]
        elif dealer_dec == 'c':
            p1_invested -= 1
            cur_pot += 1
            info_string += "Dealer calls 2, "
            if self.player:
                print(info_string)
            opp_dec = p2.make_preflop_decision(cur_pot, False, p2hc, ['x', 'r'], False)
            if opp_dec == 'x':
                info_string += "BB checks"
                if self.player:
                    print("BB checks")
                return [cur_pot, None, info_string]
            else:
                p2_invested -= 2
                cur_pot += 2
                info_string += "BB raises to 4, "
                if self.player:
                    print("BB raises to 4, ")
                dealer_dec = p1.make_preflop_decision(cur_pot, True, p1hc, ['f', 'c'], True)
                if dealer_dec == 'f':
                    info_string += "Dealer folds, BB wins pot of {0}".format(cur_pot)
                    if self.player:
                        print("Dealer folds, BB wins pot of {0}".format(cur_pot))
                    return [cur_pot, [p1_invested, p2_invested+cur_pot], info_string]
                else:
                    p1_invested -= 2
                    cur_pot += 2
                    info_string += "Dealer calls 4"
                    if self.player:
                        print("Dealer calls 4")
                    return [cur_pot, None, info_string]
        else:
            p1_invested -= 3
            cur_pot += 3
            info_string += "dealer raises to 4, "
            if self.player:
                print(info_string)
            opp_dec = p2.make_preflop_decision(cur_pot, True, p2hc, ['f', 'c'], False)
            if opp_dec == 'f':
                info_string += "BB folds, dealer wins pot of {0}".format(cur_pot)
                if self.player:
                    print("BB folds, dealer wins pot of {0}".format(cur_pot))
                return [cur_pot, [p1_invested+cur_pot, p2_invested], info_string]
            else:
                p2_invested -= 2
                cur_pot += 2
                info_string += "BB calls 4"
                if self.player:
                    print("BB calls 4")
                return [cur_pot, None, info_string]

    def showdown(self, p1hc, p2hc, bc, pot, hand_string):
        p1_fullhand = copy.deepcopy(bc)
        p2_fullhand = copy.deepcopy(bc)
        p1_fullhand.extend(p1hc)
        p2_fullhand.extend(p2hc)
        p1_rank = evaluate(p1_fullhand)
        p2_rank = evaluate(p2_fullhand)
        if self.player:
            print("SHOWDOWN")
            print("Dealer's holecards: {0} {1}".format(p1hc[0].upper(), p1hc[1].upper()))
            print("BB's holecards: {0} {1}".format(p2hc[0].upper(), p2hc[1].upper()))
        if p1_rank == p2_rank:
            msg = "Draw at showdown pot of {0} is split".format(pot)
            if self.player:
                print(msg)
            return [0,0, "{0}\n{1}".format(hand_string, msg)]
        elif p1_rank < p2_rank:
            msg = "Dealer wins pot of {0} at showdown".format(pot)
            if self.player:
                print(msg)
            return [(pot/2), -(pot/2), "{0}\n{1}".format(hand_string, msg)]
        else:
            msg = "BB wins pot of {0} at showdown".format(pot)
            if self.player:
                print(msg)
            return [-(pot/2), (pot/2), "{0}\n{1}".format(hand_string, msg)]