from deck import Card
import pandas as pd

class Player:
	def __init__(self, cards, player_id, player_name):
		self.fcard = cards[0]
		self.scard = cards[1]
		self.cards = [self.fcard, self.scard]
		self.id = player_id
		self.player_name = player_name
		self.money_invested = 5
		self.money = 0
		self.card_ranking = None
		self.table_position = None

	def is_suited(self):
		return (self.fcard.suit == self.scard.suit)

	def get_poker_cards(self):
		return self.fcard.get_pretty_print() + " " + self.scard.get_pretty_print()

	def pretty_print_cards(self):
		print("fcard: " + self.fcard.get_pretty_print())
		print("scard: " + self.scard.get_pretty_print())

	def get_card_ranking(self):
		ranking = pd.read_csv("./data/preflop_ranking.csv")

		# Determine key for searching in csv
		key =  str(self.fcard.get_poker_value() + self.scard.get_poker_value()) if self.fcard.value > self.scard.value else str(self.scard.get_poker_value() + self.fcard.get_poker_value())
		
		# Finding the card instances
		cards = ranking[ranking['card'] == key]
		card = (cards[cards["suit"] == "s"]) if self.is_suited() else (cards[cards["suit"] == "o"])

		if len(card.index) == 0:
			card = cards[cards["suit"] == "p"]

		return card.iloc[0]["rank"]

