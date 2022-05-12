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
    PORT = 8080
    SERVER = socket.gethostbyname(socket.gethostname())
    ADDR = (SERVER, PORT)
    FORMAT = "UTF-8"
    DISCONNECT_MSG = "!DISCONNECT"
    SHUTDOWN_MSG = "!SHUTDOWN"

    def __init__(self):
        self.player_count = 0
        self.board = None
        self.connections = []
        self.board_connection = None
        self.server = None
        self.board_cards = None

        # Handling the server
        while not self.server:
            try:
                self.server = self.start_server()
            except OSError:
                Server.PORT += 1
                print(Server.PORT)
                print(f"Port {Server.PORT-1} is occupied. Trying {Server.PORT}")
                time.sleep(5)
        self.server_listen()
        self.player_count = len(self.connections)

        # Detect change in board
        if not self.board_connection:
            print("Connecting failed!")
            return

        board_cards_string = self.get_board_cards()
        print(board_cards_string)
        if board_cards_string:
            # Setting up board
            deck = Deck()
            self.board_cards = [deck.get_from_deck(deck.get_values_for(card)) for card in board_cards_string.split(" ")]
            card_string = self.get_new_client_cards()
            hands = self.get_hands_from_card_string(card_string, deck)
            deck = Deck()
            players = [Player(hands[i], i) for i in range(self.player_count)]
            self.board = Board(self.player_count, players, self.board_cards) 


    def update_board(self):
        deck = Deck()
        board_cards_string = self.get_board_cards()
        board_cards = [deck.get_from_deck(deck.get_values_for(card)) for card in board_cards_string.split(" ")]
        if board_cards:
            print(board_cards)
            if len(self.board_cards) == 3 and len(board_cards) != 3:
                # New flop, last turn ended after the flop
                print("huh")

    def get_board(self):
        return self.board

    def get_board_cards(self):
        print("getting board cards")
        board_msg_length = self.board_connection.recv(Server.HEADER).decode(Server.FORMAT)
        if not board_msg_length:
            return
        board_msg_length = int(board_msg_length)
        board_msg = self.board_board_msg_length = self.board_connection.recv(board_msg_length).decode(Server.FORMAT)
        if board_msg:
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
        card_string = ""        
        for conn in self.connections:
            input("next conn")
            if not card_string:
                card_string = self.get_client_cards(conn)
                continue
            card_string += " " + self.get_client_cards(conn)
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
        self.server.settimeout(10)
        self.server.listen()

        print("Started listening for new connections")
        while running:
            # Client connects
            print(len(self.connections))
            try:
                conn, addr = self.server.accept()
                print("stopped")
                self.connections.append(conn)
                
                if not self.board_connection:
                    # Setting up connection which detects changes on board
                    self.board_connection = conn 
                    message = ("!boardConn").encode(Server.FORMAT)
                    msg_length = len(message)
                    send_length = str(msg_length).encode(Server.FORMAT)
                    send_length += b" " * (Server.HEADER - len(send_length))
                    conn.send(send_length)
                    conn.send(message)                         

            except socket.timeout:
                running = False        

        print("Stopped listening for new connections")
