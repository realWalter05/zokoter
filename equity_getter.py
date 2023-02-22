from itertools import compress, product, combinations
from random import sample

suits = ['s','d','h','c']
values = [1,2,3,4,5,6,7,8,9,10,11,12,13]

deck = [str(card[0]) + card[1] for card in list(product(values, suits))]

hand_dict ={
        0:  "Straight Flush",
        1:  "Quads",
        2:  "Full House",
        3:  "Flush",
        4:  "Straight",
        5:  "Trips",
        6:  "Two Pair",
        7:  "One Pair",
        8:  "High Card"
        }

card_dict = {
        "A": 1,
        "K": 13,
        "Q": 12,
        "J": 11,
        "T": 10,
          1: "A",
         14: "A",
         13: "K",
         12: "Q",
         11: "J"
        }

def rotate(l, n):
    return l[n:] + l[:n]

def hasConsecutive(arr, amount):
    last = 0
    count = 0
    arr = [int(txt[:-1]) for txt in arr]
    if any([num == 1 for num in arr]):
        arr = arr + [14]
    arr = sorted(arr, reverse = True)
    for i in range(len(arr)):
        if arr[i] != (last - 1) :
            count = 0
        last = arr[i]
        count += 1
        if amount <= count:
            return True, arr[i] + 4
    return False, 0

def getHand(held_cards, table_cards):
    all_cards = sorted(held_cards + table_cards)

    all_cards = [str(card_dict[card[0].upper()]) + card[-1] if card[0].isalpha() else card for card in all_cards]
    card_vals = sorted([int(txt[:-1]) for txt in all_cards], reverse = True)
    hands = [8]
    hand_cards = [sorted([14 if card == 1 else card for card in card_vals], reverse = True)[:5]]
    for suit in suits:
        suited = [suit in txt for txt in all_cards]
        if sum(suited) >= 5:
            hands.append(3)
            hand_cards.append(list(compress(card_vals, suited))[:5])
            straight, high = hasConsecutive(list(compress(all_cards, suited)), 5)
            if straight :
                hands.append(0)
                hand_cards.append([high])
            break

    straight, high = hasConsecutive(all_cards, 5)
    if straight :
        hands.append(4)
        hand_cards.append([high])

    for value in rotate(sorted(values, reverse = True),-1):
        dups = [num == value for num in card_vals]
        count_dups = sum(dups)
        if count_dups == 4:
            hands.append(1)
            hand_cards.append([[list(compress(card_vals, dups))[0]] + [list(compress(card_vals, [not i for i in dups]))[:1]]])
        elif count_dups == 3:
            hands.append(5)
            hand_cards.append([[list(compress(card_vals, dups))[0]] + list(compress(card_vals, [not i for i in dups]))[:2]])
            for value in rotate(sorted(values, reverse = True),-1):
                if value != list(compress(card_vals, dups))[0]:
                    more_dups = [num == value for num in card_vals]
                    count_dups = sum(more_dups)
                    if count_dups == 2:
                        hands.append(2)
                        hand_cards.append([[list(compress(card_vals, dups))[0]] + [list(compress(card_vals, more_dups))[0]]])
        elif count_dups == 2:
            hands.append(7)
            hand_cards.append([[list(compress(card_vals, dups))[0]] + list(compress(card_vals, [not i for i in dups]))[:3]])
            for value in rotate(sorted(values, reverse = True),-1):
                if value != list(compress(card_vals, dups))[0]:
                    more_dups = [num == value for num in card_vals]
                    count_dups = sum(more_dups)
                    if count_dups == 2:
                        hands.append(6)
                        hand_cards.append([[list(compress(card_vals, dups))[0]] + [list(compress(card_vals, more_dups))[0]] + [list(compress(card_vals, [not (dups[i] or more_dups[i]) for i in range(len(dups))]))[0]]])

    best_hand = min(hands)
    hand = hand_cards[hands.index(best_hand)]

    return best_hand, hand

def compareHands(our_hand, our_highs, opp_hand, opp_highs):
    if our_hand < opp_hand:
        return "W"
    elif our_hand > opp_hand:
        return "L"
    elif our_hand == opp_hand:
        for i in range(len(our_highs)):
            if our_highs[i] > opp_highs[i]:
                return "W"
            elif our_highs[i] < opp_highs[i]:
                return "L"
        return "D"

def Check_Odds(our_cards, table_cards = []):
    unseen_deck = [card for card in deck if not (card in (our_cards + table_cards))]
    results = []
    unseen_combs = list(combinations(unseen_deck,5-len(table_cards)))
    for tableCards in sample(unseen_combs, int(min(1e2,len(unseen_combs)))):
        undrawn_deck = [card for card in unseen_deck if not (card in list(tableCards))]
        undrawn_combs = list(combinations(undrawn_deck,2))
        our_hand, our_highs = getHand(our_cards, table_cards + list(tableCards))
        for oppCards in sample(undrawn_combs, int(min(1e3,len(undrawn_combs)))):
            opp_hand, opp_highs = getHand(list(oppCards), table_cards + list(tableCards))
            results.append(compareHands(our_hand, our_highs, opp_hand, opp_highs))

    wins = sum([result == "W" for result in results])
    total = len(results)
    odds = wins/total
    return odds

def get_equity(hand, board):
    equity = round(100*Check_Odds(hand, board), 2)
    return equity