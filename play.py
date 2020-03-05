from bot import Bot
from game import Game

def setup_game():
    print("Starting a game of Heads up Limit Poker")
    userplay = input("Input 1 to play yourself, or any other key to see 2 bots play")
    if userplay == '1':
        oppstyle = '0'
        while(oppstyle not in ['1','2','3','4']):
            oppstyle = input("Pick a style for your opponent: \n1 - Loose Aggressive \
                \n2 - Loose Passive\n3 - Tight Aggressive\n4 - Tight Passive")
        g = Game(True,[Bot(oppstyle)])
        g.begin()
    else:
        bot1style = '0'
        while(bot1style not in ['1','2','3','4']):
            bot1style = input("Pick a style for Bot 1: \n1 - Loose Aggressive \
                \n2 - Loose Passive\n3 - Tight Aggressive\n4 - Tight Passive")
        bot2style = '0'
        while(bot2style not in ['1','2','3','4']):
            bot2style = input("Pick a style for Bot 2: \n1 - Loose Aggressive \
                \n2 - Loose Passive\n3 - Tight Aggressive\n4 - Tight Passive")
        numhands = 'a'
        while(not numhands.isdigit()):
        	numhands = input("How many hands would you like to be played?")
        g = Game(False,[Bot(bot1style), Bot(bot2style)], int(numhands))
        g.begin()

setup_game()