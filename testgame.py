from gameplay import Game
import time
import sys

#default values
player = False
lb = False
hands = 10
hands_per_save = 100
bot_player = None
bot_opp = None

if(len(sys.argv)>1):
    if(sys.argv[1].upper() == "Y"):
        player = True
if(len(sys.argv)>2):
    if(sys.argv[2].upper() == "Y"):
        lb = True
if(len(sys.argv)>3):
    hands = int(sys.argv[3])
if(len(sys.argv)>4):
    hands_per_save = int(sys.argv[4])
if(len(sys.argv)>5):
    bot_player = sys.argv[5]
if(len(sys.argv)>6):
    bot_opp = sys.argv[6]

a = Game(player, lb, bot_player, bot_opp)
b = time.time()
a.start(hands, hands_per_save)
print(time.time() - b)