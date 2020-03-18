from bot import Bot
from datetime import datetime
import evaluator
import random

class Player:
    def __init__(self):
        print("Welcome to the game, good luck")

    def make_decision(self, pot, current_bet, hand, board, options):
        print("\nYour Hand: {0} {1}".format(hand[0].upper(), hand[1].upper()))
        print("Board: {0}".format((', '.join(board)).upper()))
        print("Pot: {0}. Current Bet: {1}".format(pot, current_bet))
        dec = input("What action do you take? {0}\n".format(options))
        while dec not in options:
            print("You must enter one of the options - {0}".format(options))
            dec = input("What action do you take? {0}".format(options))
        return dec

    def make_preflop_decision(self, pot, raise_made, hand, options, dealer):
        print("\nYour Hand: {0} {1}".format(hand[0].upper(), hand[1].upper()))
        dec = input("What action do you take? {0}\n".format(options))
        while dec not in options:
            print("You must enter one of the options - {0}".format(options))
            dec = input("What action do you take? {0}\n".format(options))
        return dec