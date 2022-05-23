from threading import Thread
from deck import Deck, Card
from player import Player
import holdem_calc 
import time

class Board:
	def __init__(self, player_count, players, board, deck):
		print("Board created :)")
		self.deck = deck
		self.player_count = player_count
		self.players = players
		self.board_cards = board
		self.player_odds = self.get_players_odds() if len(board) > 0 else []
		
	def add_to_board(self, card):
		self.board_cards.append(card)
		self.player_odds = self.get_players_odds() if len(self.board_cards) > 0 else []

	def get_pretty_print_board(self):
		return (" ".join([card.get_pretty_print() for card in self.board_cards]))

	def get_players_odds(self): 
		players = [(card.get_poker_value() + card.get_poker_suit()) for player in self.players for card in player.cards]
		print([i for i in self.board_cards])
		board = [(card.get_poker_value() + card.get_poker_suit()) for card in self.board_cards]

		odds = holdem_calc.calculate(board, True, 1, None, players, False)
		return odds 

	def get_best_player_odds(self):
		return max(self.player_odds)

	def get_player_odds(self, player_id):
		return self.player_odds[player_id + 1]

	def get_available_combinations(self):
		deck_cards = [*self.deck.available_cards]
		combinations = []
		for first_card in deck_cards:
			deck = deck_cards
			deck.remove(first_card)

			for second_card in deck:
				deck_without_cards = deck
				deck_without_cards.remove(second_card)

				for third_card in deck_without_cards:
					final_deck_without_cards = deck_without_cards
					final_deck_without_cards.remove(third_card)	

					if len(self.board_cards) == 3:
							for fourt_card in final_deck_without_cards:					
								for combination in self.get_absolutely_all_combinations([*self.board_cards, Card(first_card), Card(second_card)], [Card(third_card), Card(fourt_card)]):
									if combination not in combinations:
										combinations.append(combination)		
					
					elif len(self.board_cards) == 4:
						for combination in self.get_absolutely_all_combinations([*self.board_cards, Card(first_card)], [Card(second_card), Card(third_card)]):
							if combination not in combinations:
								combinations.append(combination)

		return sorted(combinations)

	def get_opponent_cards_data(self):
		opponent_data = {"best_odds": 0,"best_cards": 0, "lower_odds_count": 0,"all_odds_count": 0, "available_combinations": []}
		players = [(card.get_poker_value() + card.get_poker_suit()) for player in self.players for card in player.cards]
		board = [(card.get_poker_value() + card.get_poker_suit()) for card in self.board_cards]

		def get_odds(origin, available_cards):
			for fcard_value in origin:
				deck = available_cards
				deck.remove(fcard_value)	
				
				for scard_value in deck:
					opponent_data["all_odds_count"] += 1
					fcard = Card(fcard_value)
					scard = Card(scard_value)
					check_cards = [*players, (fcard.get_poker_value() + fcard.get_poker_suit()), (scard.get_poker_value() + scard.get_poker_suit())]
					odds = holdem_calc.calculate(board, False, 1, None, check_cards, False)

					if odds[len(odds)-1] > opponent_data["best_odds"]:
						opponent_data["best_odds"] = odds[len(odds)-1]
						opponent_data["best_cards"] = (fcard.get_poker_value() + fcard.get_poker_suit()), (scard.get_poker_value() + scard.get_poker_suit())
					
					if odds[len(odds)-1] < self.get_best_player_odds():
						opponent_data["lower_odds_count"] += 1

		# Multi-threading
		cards = [*self.deck.available_cards]
		decks = [cards[i:i + 4] for i in range(0, len(cards), 4)]
		max_threads = len(decks)
		
		threads = []
		for i in range(0, max_threads):
			t = Thread(target=get_odds, args=[decks[i], cards])
			t.start()
			threads.append(t)
		
		for t in threads:
			t.join()

		opponent_data["available_combinations"] = self.translate_combinations_to_string(self.get_available_combinations())

		return opponent_data

	def prettify_board(self):
		print("\nBoard")
		for card in self.board_cards:
			print(card.get_pretty_print())

	def prettify_game(self):
		for player in self.players:
			print("\nPlayer " + str(player.id))
			player.pretty_print_cards()
			boardss = [card.get_poker_value() + card.get_poker_suit() for card in self.board_cards]

			print(self.get_player_odds(player.id))
			print([self.translate_combination(combination) for combination in self.get_combinations(self.board_cards, player.cards)])

		self.prettify_board()

	def translate_combination(self, combination):
		combinations = {9 : "Royal flush", 8 : "Straight flush", 7 : "Four of kind", 6 : "Full house", 5 : "Flush", 4 : "Straight", 3 : "Three of kind", 2 : "Two pair", 1 : "One pair", 0 : "High card"}
		return combinations[combination]		

	def translate_combinations_to_string(self, combinations):
		translated = [self.translate_combination(combination) for combination in combinations]
		result = ', '.join([str(comb) for comb in translated])
		return result

	def get_combinations(self, board, hand):
		suits = [card.suit for card in board] + [hand[0].suit, hand[1].suit]
		values = [card.value for card in board] + [hand[0].value, hand[1].value]
		same_suit_count = max([suits.count(s) for s in suits])
		sorted_values = sorted(values)
		same_cards = sorted([values.count(value) for value in set(values)])
		player_has = []

		def is_flush():
			if same_suit_count > 4:
				return True
			return False

		def is_straight():
			set_values = list(set(sorted_values))
			straight_order = 0

			if 0 in set_values and 1 in set_values and 2 in set_values and 3 in set_values and 12 in set_values:
			# Exception for A straight
				return True

			for i in range(len(set_values)):	
				if len(set_values) - i > 4:	
					for j in range(i, i+4):	
						if (set_values[j+1] - set_values[j]) == 1:
							straight_order += 1
							continue
						straight_order = 0

			straight = True if straight_order > 4 else False
			return straight

		if is_straight() and is_flush():
			if sorted_values[-1] == 12:
				# Royal flush
				player_has.append(9)
			if 9 not in player_has:
				# Straight flush 
				player_has.append(8)

		if is_flush() and 9 not in player_has and 8 not in player_has:
			player_has.append(5)

		if is_straight() and 9 not in player_has:
			player_has.append(4)

		if 4 in same_cards:
			player_has.append(7)

		if 3 in same_cards and 2 in same_cards:
			player_has.append(6)

		if 3 in same_cards and 6 not in player_has:
			player_has.append(3)

		if same_cards.count(2) == 2:
			player_has.append(2)

		if same_cards.count(2) == 1 and 6 not in player_has:
			player_has.append(1)
		
		player_has.append(0)
		return player_has

	def get_absolutely_all_combinations(self, board, hand):
		suits = [card.suit for card in board] + [hand[0].suit, hand[1].suit]
		values = [card.value for card in board] + [hand[0].value, hand[1].value]
		same_suit_count = max([suits.count(s) for s in suits])
		sorted_values = sorted(values)
		same_cards = sorted([values.count(value) for value in set(values)])
		player_has = []

		def is_flush():
			if same_suit_count > 4:
				return True
			return False

		def is_straight():
			set_values = list(set(sorted_values))
			straight_order = 0

			if 0 in set_values and 1 in set_values and 2 in set_values and 3 in set_values and 12 in set_values:
			# Exception for A straight
				return True

			for i in range(len(set_values)):	
				if len(set_values) - i > 4:	
					for j in range(i, i+4):	
						if (set_values[j+1] - set_values[j]) == 1:
							straight_order += 1
							continue
						straight_order = 0

			straight = True if straight_order > 4 else False
			return straight

		if is_straight() and is_flush():
			if sorted_values[-1] == 12:
				# Royal flush
				player_has.append(9)
			if 9 not in player_has:
				# Straight flush 
				player_has.append(8)

		if is_flush():
			player_has.append(5)

		if is_straight():
			player_has.append(4)

		if 4 in same_cards:
			player_has.append(7)

		if 3 in same_cards and 2 in same_cards:
			player_has.append(6)

		if 3 in same_cards:
			player_has.append(3)

		if same_cards.count(2) == 2:
			player_has.append(2)

		if same_cards.count(2) == 1:
			player_has.append(1)
		
		player_has.append(0)
		return player_has		

	def get_opponent_winnability(self, opponent_combinations, players):
		player_combinations = [player["combinations"] for player in players.values()]
		combinations = [comb for combination in player_combinations for comb in combination]
		
		if not opponent_combinations:
			# Game already won for our player
			return False

		if max(opponent_combinations) < max(combinations):
			return False
		return True

	def get_player_rank(self, player_id):
		player_odds = sorted(self.player_odds[1:])
		player_value = self.get_player_odds(player_id)
		return player_odds.index(player_value)

	def format_player_data(self):
		players = {}
		print(self.board_cards)
		for player in self.players:
			players[player.id] = {
				"player_odds" : ("%.2f " % (round(self.get_player_odds(player.id), 2) * 100)) if len(self.board_cards) > 0 else "xxx",
				"player_cards" : player.get_poker_cards(),
				"combinations" : self.translate_combinations_to_string(self.get_combinations(self.board_cards, player.cards)),
				"preflop_rank" : player.get_card_ranking(),
				"table_position" : player.table_position,
				"rank" : self.get_player_rank(player.id) if len(self.board_cards) > 0 else 0,
				"player_money" : player.money
			}
		return players

	def format_opponent_data(self, players):
		opponent_data = self.get_opponent_cards_data()
		opponent = {
			"best_odds" : round(opponent_data["best_odds"], 2) * 100,
			"best_cards" : opponent_data["best_cards"],
			"lower_odds_count" : opponent_data["lower_odds_count"],
			"all_odds_count" : opponent_data["all_odds_count"],
			"better_odds" : 100 - round((opponent_data["lower_odds_count"] / opponent_data["all_odds_count"]), 2) * 100,
			"combinations" : opponent_data["available_combinations"],
			"winnable" : self.get_opponent_winnability(opponent_data["available_combinations"], players),
			"table_position" : 3
		}
		return opponent

#if __name__ == "__main__":
#	# Setup game
#	for i in range(3):
#		deck = Deck()
#		player_count = 2
#		players = [deck.draw_hand() for i in range(player_count)]
#		board = [deck.get_card() for i in range(3)]    
#		b = Board(player_count, players, board, deck)
#	
#		default = len(b.deck.available_cards)		
#		print("Default " + str(default))
#		for i in range(1):
#			b.format_data()
#			print(len(b.deck.available_cards))



