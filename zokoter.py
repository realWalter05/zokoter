from flask import Flask, jsonify, render_template
from server import Server
# TODO zrusit recheck (uploadnout client z druhyho pc na github)
# TODO neco se detect difference
# TODO a maybe tam je nejakej bug ze kdyz se odpoji hraci, tak to pak nemuze spocitat odds nebo tak neco
# TODO kdyz je pridana karta zeptat se na to kolik ma typek callnout a vypocit EV
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

@app.route("/opponent", methods=["POST"])
def opponent():
    board = server.get_board()   
    board_player_data = board.format_player_data()
    board_opponent_data = board.format_opponent_data(board_player_data) if len(board.board_cards) else None
    return jsonify(board_opponent_data)

@app.route("/whitepaper")
def whitepaper():
    return render_template("whitepaper.html") 

@app.route("/board_update")
def board_update():
    try:
        # 'Handling' all kind of exceptions lol
        server.update_board()
    except Exception as e:
        print(f"Zokoter error occured: {e} Reset the page by logo click!")

    board = server.get_board()   
    board_opponent_data = None
    return render_template("index.html", players=board.format_player_data(), opponent=board_opponent_data, board=board.get_pretty_print_board())    


if __name__ == "__main__": 
    app.run()
