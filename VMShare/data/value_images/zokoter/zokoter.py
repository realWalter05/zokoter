from flask import Flask, render_template
from server import Server

app = Flask(__name__)
board = Server().get_board()

@app.route("/")
def index():
    board_player_data = board.format_player_data()
    board_opponent_data = board.format_opponent_data(board_player_data)
    return render_template("index.html", players=board_player_data, opponent=board_opponent_data, board=board.get_pretty_print_board())    

if __name__ == "__main__":
    app.run(debug=True)
