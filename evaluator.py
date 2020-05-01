from lookup import Lookups

from operator import __or__, __xor__
from functools import reduce
from itertools import combinations
from collections import Counter
import math

GRID = [0] * 2**16
for i in range(len(GRID)):
    GRID[i] = (i & 1) + GRID[i >> 1]

def bin_conversion(card):
    #Schema for binary representation of card - adaptation of Cactus Kev's/RadekJ's

    #---bbbbb bbbbbbbb --pppppp ssssvvvv

    #b - bit turned on for for the value from ace to deuce
    #p - prime representation of the value, 2 for Deuce, up to 41 for Ace
    #s - suit of the card represented as a prime, 2-Clubs, 3-Spades, 5-Hearts, 7-Diamonds
    #v - value of the card starting with Deuce - 0, up to Ace - 12

    if len(card) != 2 and card[0:2] != "10":
        raise Exception("card must be in format value then suit; 2d, 6h, Ks, Ad, 10h")

    card_tables = Lookups.CardLookups

    suit_mask = card_tables.STRING_TO_SUIT[card[-1]] << 4

    rank = card[:-1]

    if rank.upper() not in ["A", "K", "Q", "J"]:
        rank_index = int(rank) - 2 
    else:
        rank_index = card_tables.PICTURE_TO_RANK[rank.upper()]

    bit_mask = 2**(rank_index + 16)

    prime_mask = card_tables.PRIME_NUMBERS[rank_index] << 8

    return bit_mask | prime_mask | suit_mask | rank_index

def evaluate(hand):
    #bin_hand is an array of ints - a binary representation of the hand
    bin_hand = [i for i in map(bin_conversion, hand)]
    river = False
    turn = False
    flop = False
    if len(hand) == 7:
        tables = Lookups.EvalLookups.River
        river = True
    elif len(hand) == 6:
        tables = Lookups.EvalLookups.Turn
        turn = True
    elif len(hand) == 5:
        tables = Lookups.EvalLookups.Flop
        flop = True
    else:
        return -1

    #f_product is product of all suit's in hand after primes multiplied
    f_product = 1
    for c in bin_hand:
        f_product = f_product * ((c & 240) >> 4)

    #check for flush first regardless of how many cards
    (flush_bool, flush_suit) = check_flush(f_product)

    odd_xor = reduce(__xor__, bin_hand) >> 16
    even_xor = (reduce(__or__, bin_hand) >> 16) ^ odd_xor

    if flop:
        unique_cards = (reduce(__or__, bin_hand) >> 16)
        if flush_bool:
            return tables.flushes[unique_cards]
        else:
            rank = tables.unique[unique_cards]
            if rank == 0:
                p_product = 1
                for c in bin_hand:
                    p_product = p_product * ((c & 16128) >> 8)
                rank = tables.non_unique.get(p_product)
            return rank

    if flush_bool:
        if even_xor == 0:
            bits = reduce(__or__, map(
                lambda card: (card >> 16),
                filter(
                    lambda card: (card >> 4) & 15 == flush_suit, bin_hand)))
            return tables.flush_rank_bits_to_rank[bits]
        else:
            if river:
                even_counter = count_bits(even_xor)
                if even_counter == 2:
                    return tables.flush_rank_bits_to_rank[odd_xor | even_xor]
                else:
                    bits = reduce(__or__, map(
                        lambda card: (card >> 16),
                        filter(
                            lambda card: (card >> 4) & 15 == flush_suit, bin_hand)))
                    return tables.flush_rank_bits_to_rank[bits]
            else:
                return tables.flush_rank_bits_to_rank[odd_xor | even_xor]

    odd_bits = count_bits(odd_xor)
    even_bits = count_bits(even_xor)
    if river:
        if even_xor == 0:
            if odd_bits == 7:
                return tables.odd_xors_to_rank[odd_xor]
            else:
                #p_product is product of all prime values multiplied
                p_product = 1
                for c in bin_hand:
                    p_product = p_product * ((c & 16128) >> 8)
                return tables.prime_products_to_rank[p_product]
        else:
            if odd_bits == 5:
                return tables.even_xors_to_odd_xors_to_rank[even_xor][odd_xor]
            elif odd_bits == 3:
                if even_bits == 2:
                    return tables.even_xors_to_odd_xors_to_rank[even_xor][odd_xor]
                else: 
                    #p_product is product of all prime values multiplied
                    p_product = 1
                    for c in bin_hand:
                        p_product = p_product * ((c & 16128) >> 8)
                    return tables.prime_products_to_rank[p_product]
            else:
                even_bits = count_bits(even_xor)
                if even_bits == 3:
                    return tables.even_xors_to_odd_xors_to_rank[even_xor][odd_xor]
                elif even_bits == 2:
                    #p_product is product of all prime values multiplied
                    p_product = 1
                    for c in bin_hand:
                        p_product = p_product * ((c & 16128) >> 8)
                    return tables.prime_products_to_rank[p_product]
                else:
                    return tables.even_xors_to_odd_xors_to_rank[even_xor][odd_xor]
    elif turn:
        if even_xor == 0:
            if odd_bits != 4:
                return tables.odd_xors_to_rank[odd_xor]
            else:
                p_product = 1
                for c in bin_hand:
                    p_product = p_product * ((c & 16128) >> 8)
                return tables.prime_products_to_rank[p_product]
        elif odd_xor == 0:
            if even_bits != 2:
                return tables.even_xors_to_rank[even_xor]
            else:
                p_product = 1
                for c in bin_hand:
                    p_product = p_product * ((c & 16128) >> 8)
                return tables.prime_products_to_rank[p_product]
        else:
            if odd_bits == 4:
                return tables.even_xors_to_odd_xors_to_rank[even_xor][odd_xor]
            else:
                if even_bits == 2:
                    return tables.even_xors_to_odd_xors_to_rank[even_xor][odd_xor]
                else:
                    p_product = 1
                    for c in bin_hand:
                        p_product = p_product * ((c & 16128) >> 8)
                    return tables.prime_products_to_rank[p_product]


def check_flush(x, flush_cards=5):
    for suit in [2, 3, 5, 7]:
        if x % (suit**flush_cards) == 0:
            return (True, suit)
    return (False, 0)


def percentile(hc, board, rank):
    #Rank Percentiles - will be rounded down to nearest 0.05
    #0 - 0.00
    #1 - 0.05
    #...
    #18 - 0.90
    #19 - 0.95
    deck = set(Lookups.EvalLookups.deck)
    all_hands = list(combinations(deck - set(hc) - set(board), 2))
    beaten = 0.0
    for h in all_hands:
        r = evaluate(board + list(h))
        if r > rank:
            beaten += 1.0
        elif r == rank:
            beaten += 0.5
    if beaten/len(all_hands) == 1.0:
        return 19
    else:
        return int(math.floor((beaten/len(all_hands)) / 0.05))


def board_texture(board):
    #Board Texture values:
    #0 - Unique Rainbow
    #1 - 3 to a Flush
    #2 - 4 to a Straight
    #3 - Paired
    #4 - 3 to a Flush + Paired
    #5 - 4 to a Flush
    #6 - Double Paired
    #7 - Trips
    texture = 0
    bin_board = [i for i in map(bin_conversion, board)]
    #f_product is product of all suit's in hand after primes multiplied
    f_product = 1
    for c in bin_board:
        f_product = f_product * ((c & 240) >> 4)

    #check for any flushes first
    (flush_bool, flush_suit) = check_flush(f_product, 4)
    if flush_bool:
        return 5
    else:
        (flush_bool, flush_suit) = check_flush(f_product, 3)
        if flush_bool:
            texture += 1

    unsuited_board = [x[:-1] for x in board]

    if check_four_straight(unsuited_board):
        return 2

    counts = Counter(unsuited_board).values()
    if 3 in counts:
        return 7
    elif list(counts).count(2) == 2:
        return 6
    elif 2 in counts:
        return texture+3
    else:
        return texture


def check_four_straight(l):
    ints = {"2":[2],"3":[3],"4":[4],"5":[5],"6":[6],"7":[7],"8":[8],"9":[9],"10":[10],
            "j":[11],"J":[11],"q":[12],"Q":[12],"k":[13],"K":[13],"a":[14,1],"A":[14,1]}
    if len(l) < 4:
        return False
    else:
        int_list_board = [ints[x] for x in l]
        int_board = [item for sublist in int_list_board for item in sublist]
        possible_straights = list(combinations(int_board, 4))
        for s in possible_straights:
            straight = list(range(min(s), max(s)+1))
            if set(s) == set(straight) and len(set(straight)) == 4:
                return True
    return False


def hand_strength(x):
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
    hand_strengths = [6185, 3325, 2467, 1609, 1599, 322, 166, 10]
    i = 0
    for a in hand_strengths:
        if x > a:
            return i
        i += 1
    return i


def count_bits(x):
    return GRID[x & 0xffff] + GRID[(x >> 16) & 0xffff]


