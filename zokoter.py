from flask import Flask, render_template
from server import Server

app = Flask(__name__)
server = Server()
board = server.get_board()
board_player_data = board.format_player_data()

@app.route("/")
def index():
    board_opponent_data = None
    return render_template("index.html", players=board_player_data, opponent=board_opponent_data, board=board.get_pretty_print_board())    

@app.route("/opponent")
def opponent():
    board_opponent_data = board.format_opponent_data(board_player_data) if len(board.board_cards) else None
    return render_template("index.html", players=board_player_data, opponent=board_opponent_data, board=board.get_pretty_print_board())    


@app.route("/check_board")
def opponent():
    board_opponent_data = board.format_opponent_data(board_player_data) if len(board.board_cards) else None
    return render_template("index.html", players=board_player_data, opponent=board_opponent_data, board=board.get_pretty_print_board())    


if __name__ == "__main__":
    app.run(debug=True)
