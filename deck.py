import random

class Card:
	poker_values = {
		0 : "2",
		1 : "3",
		2 : "4",
		3 : "5",
		4 : "6",
		5 : "7",
		6 : "8",
		7 : "9",
		8 : "T",
		9 : "J",
		10 : "Q",
		11 : "K",
		12 : "A"
	}
	poker_suits = {
		0 : "h",
		1 : "s",
		2 : "d",
		3 : "c",
	}
	poker_suit_emojis = {
		0 : "♥",
		1 : "♠️",
		2 : "♦️",
		3 : "♣️",
	}	

	def __init__(self, card):
		self.value = card[0]
		self.suit = card[1]

	def get_poker_value(self):
		return Card.poker_values[self.value]

	def get_poker_suit(self):
		return Card.poker_suits[self.suit]

	def get_pretty_print(self):
		return (self.get_poker_value() + Card.poker_suit_emojis[self.suit])


class Deck:
	def __init__(self):
		self.cards = [
			# Hearts - sdrce
			(0, 0),
			(1, 0),
			(2, 0),
			(3, 0),
			(4, 0),
			(5, 0),
			(6, 0),
			(7, 0),
			(8, 0),
			(9, 0),
			(10, 0),
			(11, 0),
			(12, 0),
			# Spades - listy
			(0, 1),
			(1, 1),
			(2, 1),
			(3, 1),
			(4, 1),
			(5, 1),
			(6, 1),
			(7, 1),
			(8, 1),
			(9, 1),
			(10, 1),
			(11, 1),
			(12, 1),
			# Diamonds - káry
			(0, 2),
			(1, 2),
			(2, 2),
			(3, 2),
			(4, 2),
			(5, 2),
			(6, 2),
			(7, 2),
			(8, 2),
			(9, 2),
			(10, 2),
			(11, 2),
			(12, 2),
			# Clubs - piky
			(0, 3),
			(1, 3),
			(2, 3),
			(3, 3),
			(4, 3),
			(5, 3),
			(6, 3),
			(7, 3),
			(8, 3),
			(9, 3),
			(10, 3),
			(11, 3),
			(12, 3)
		]	
		self.available_cards = [*self.cards]
		self.dead_cards = []

	def get_values_for(self, poker_name):
		values_key_list = list(Card.poker_values.keys())
		values_values_list = list(Card.poker_values.values())
		tuple_value = values_key_list[values_values_list.index(poker_name[0])]

		suit_key_list = list(Card.poker_suits.keys())
		suit_values_list = list(Card.poker_suits.values())
		tuple_suit = suit_key_list[suit_values_list.index(poker_name[1])]
				
		result = (tuple_value, tuple_suit)
		return result


	def draw_card(self):
		card = random.choice(self.available_cards)
		self.available_cards.remove(card)
		self.dead_cards.append(card)
		return card

	def get_from_deck(self, values):
		self.available_cards.remove(values)
		self.dead_cards.append(values)
		return Card(values)	

	def get_card(self):
		return Card(self.draw_card())

	def draw_hand(self):
		return (self.get_card(), self.get_card())


