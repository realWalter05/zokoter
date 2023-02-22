from board import Board
from player import Player
from deck import Deck
from multiprocessing.connection import Listener


class Server:
    def __init__(self):
        print("Server activated")
        deck = Deck()
        player_count = 3
        players = [Player(deck.draw_hand(), i) for i in range(player_count)]
        board = [deck.get_card() for i in range(3)]
        #self.board_cards = [self.deck.get_from_deck(self.deck.get_values_for("2c")), self.deck.get_from_deck(self.deck.get_values_for("5c")), \
        #                   self.deck.get_from_deck(self.deck.get_values_for("7d")), self.deck.get_from_deck(self.deck.get_values_for("As"))]        
        self.board = Board(player_count, players, board, deck)
        #self.setup_server()

    def get_board(self):
        return self.board

    def setup_server(self):
        address = ('localhost', 6000)   
        listener = Listener(address, authkey=b'&oi}Po5e6')
        conn = listener.accept()
        print('connection accepted from', listener.last_accepted)
        while True:
            msg = conn.recv()
            # do something with msg
            print(msg)
            if msg == 'close':
                conn.close()
                break
        listener.close()        
