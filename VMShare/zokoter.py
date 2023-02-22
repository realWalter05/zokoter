from flask import Flask, render_template
from server import Server

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("setup.html")    

@app.route("/setup")
def setup():
    global server
    server = Server()
    board = server.get_board()   
    board_opponent_data = None
    return render_template("index.html", players=board.format_player_data(), opponent=board_opponent_data, board=board.get_pretty_print_board()) 

@app.route("/opponent")
def opponent():
    board = server.get_board()   
    board_player_data = board.format_player_data()
    board_opponent_data = board.format_opponent_data(board_player_data) if len(board.board_cards) else None
    return render_template("index.html", players=board_player_data, opponent=board_opponent_data, board=board.get_pretty_print_board())    


@app.route("/board_update")
def board_update():
    board = server.get_board()   
    print("before update")
    print(board.format_player_data())
    server.update_board()
    board = server.get_board()   
    print("after update")
    print(board.format_player_data())
    board_opponent_data = None
    return render_template("index.html", players=board.format_player_data(), opponent=board_opponent_data, board=board.get_pretty_print_board())    


if __name__ == "__main__": 
    app.run(debug=True)