from lookup import Lookups

from operator import __or__, __xor__
from functools import reduce

GRID = [0] * 2**16
for i in range(len(GRID)):
    GRID[i] = (i & 1) + GRID[i >> 1]

def bin_conversion(card):
    #Schema for binary representation of card - adaptation of Cactus Kev's/RadekJ

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

    tables = Lookups.EvalLookups

    #f_product is product of all suit's in hand after primes multiplied
    f_product = 1
    for c in bin_hand:
        f_product = f_product * ((c & 240) >> 4)

    #check for flush first
    (flush_bool, flush_suit) = check_flush(f_product)
    
    odd_xor = reduce(__xor__, bin_hand) >> 16
    even_xor = (reduce(__or__, bin_hand) >> 16) ^ odd_xor

    if flush_bool:
        even_counter = count_bits(even_xor)
        if even_xor == 0:
            bits = reduce(__or__, map(
                lambda card: (card >> 16),
                filter(
                    lambda card: (card >> 4) & 15 == flush_suit, bin_hand)))
            return tables.flush_rank_bits_to_rank[bits]
        else:
            if even_counter == 2:
                return tables.flush_rank_bits_to_rank[odd_xor | even_xor]
            else:
                bits = reduce(__or__, map(
                    lambda card: (card >> 16),
                    filter(
                        lambda card: (card >> 4) & 15 == flush_suit, bin_hand)))
                return tables.flush_rank_bits_to_rank[bits]

    odd_bits = count_bits(odd_xor)
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
            even_bits = count_bits(even_xor)
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

def check_flush(x):
    for suit, factor in [(2, 32), (3, 243), (5, 3125), (7, 16807)]:
        if x % factor == 0:
            return (True, suit)
    return (False, 0)

def count_bits(x):
    return GRID[x & 0xffff] + GRID[(x >> 16) & 0xffff]

print(evaluate(['ac','9h','qc','jc','10c', '9d', '2h']))