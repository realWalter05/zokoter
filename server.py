from board import Board
from player import Player
from deck import Deck
from multiprocessing.connection import Listener
import socket
import time
import threading


class Server:
    # Define data
    HEADER = 64
    PORT = 7849
    SERVER = ""
    ADDR = (SERVER, PORT)
    FORMAT = "UTF-8"

    def __init__(self):
        self.player_count = 0
        self.board = None
        self.connections = []
        self.player_names = []
        self.board_connection = None
        self.server = None
        self.board_cards = None

        # Handling the server
        print(f"Server address {Server.ADDR} and port {Server.PORT}")
        while not self.server:
            try:
                self.server = self.start_server()
            except OSError:
                print(f"Port {Server.PORT-1} is occupied. Trying {Server.PORT}")
                return
        self.server_listen()

        self.player_count = len(self.connections)
        # Detect change in board
        if not self.board_connection:
            print("Connecting failed!")
            return

        board_cards_string = self.get_board_cards()
        print(f"Board cards: {board_cards_string}")
        # Setting up board
        self.board = self.get_new_board(board_cards_string)


    def get_new_board(self, board_cards_string):
        deck = Deck()
        self.board_cards = []
        if board_cards_string:
            # If board is not empty
            self.board_cards = [deck.get_from_deck(deck.get_values_for(card)) for card in board_cards_string.split(" ")]
        card_string = self.get_new_client_cards()
        print(card_string)
        if not card_string:
            return None
        hands = self.get_hands_from_card_string(card_string, deck)
        player_count = len(hands)
        players = [Player(hands[i], i, self.player_names[i]) for i in range(player_count)]
        return Board(player_count, players, self.board_cards, deck) 

    def update_board(self):
        board_updated = False
        while not board_updated:    
            deck = Deck()
            board_cards_string = self.get_board_cards()
            board_cards = []
            if board_cards_string:
                board_cards = [deck.get_from_deck(deck.get_values_for(card)) for card in board_cards_string.split(" ")]

            if not self.board_cards and len(board_cards) == 3 or len(self.board_cards) > 0 and len(board_cards) == 0 or len(self.board_cards) == 0 and len(board_cards) == 0:
                # First flop ever
                print("New round")
                board = self.get_new_board(board_cards_string)   
                if board:
                    self.board = board                   
                    board_updated = True                      
            elif len(self.board_cards) < len(board_cards):
                # Card added
                print("Card added")
                self.board.add_to_board(board_cards[len(board_cards) - 1])
                board = self.get_new_board(board_cards_string)   
                if board:
                    self.board = board                   
                    board_updated = True                   


    def get_board(self):
        return self.board

    def get_board_cards(self):
        print("getting board cards")
        # Send request for boaard cards
        message = ("!boardConn").encode(Server.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(Server.FORMAT)
        send_length += b" " * (Server.HEADER - len(send_length))
        self.board_connection.send(send_length)
        self.board_connection.send(message)           

        # Receiving the cards
        board_msg_length = self.board_connection.recv(Server.HEADER).decode(Server.FORMAT)
        if not board_msg_length:
            return
        board_msg_length = int(board_msg_length)
        board_msg = self.board_board_msg_length = self.board_connection.recv(board_msg_length).decode(Server.FORMAT)
        if board_msg or board_msg == "":
            print(f"Board cards has changed. New cards are {board_msg}")
            return board_msg
        return

    def get_hands_from_card_string(self, card_string, deck):
        card_values = [deck.get_from_deck(deck.get_values_for(card)) for card in card_string.split(" ")]
        hands = []
        i = 0
        while i in range(len(card_values)):
            hands.append((card_values[i], card_values[i+1]))
            i += 2
        return hands

    def get_new_client_cards(self):
        card_list = []     
        for conn in self.connections:
            #input("Scan cards on enter: ")

            cards = self.get_client_cards(conn)
            if cards == "":
                # Some player folded
                continue
            card_list.append(cards)

        card_string = " ".join(card_list)
        return card_string

    def get_client_cards(self, conn):
        # Ask for cards
        message = ("!sendcards").encode(Server.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(Server.FORMAT)
        send_length += b" " * (Server.HEADER - len(send_length))
        conn.send(send_length)
        conn.send(message)    

        # Receive new card
        msg_length = conn.recv(Server.HEADER).decode(Server.FORMAT)
        if not msg_length:
            return
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(Server.FORMAT)
        return msg
    
    def close_server(self):
        self.server.shutdown(socket.SHUT_RDWR)
        self.server.close()
        print("Server closed")

    def start_server(self):
        print("Server started")        
        # Bind socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(Server.ADDR)
        return server

    def server_listen(self):
        running = True
        self.server.settimeout(120)
        self.server.listen()

        print("Started listening for new connections")
        while running:
            # Client connects
            try:
                conn, addr = self.server.accept()
                print(f"Player {len(self.connections)} connected")
                self.connections.append(conn)
                self.player_names.append(input("Player name: "))
                
                if not self.board_connection:
                    # Setting up connection which detects changes on board
                    self.board_connection = conn          

                if len(self.connections) > 1:
                    if input("Type exit to stop listening: ") == "exit":
                        running = False                           

            except socket.timeout:
                running = False        
        print("Stopped listening for new connections")
