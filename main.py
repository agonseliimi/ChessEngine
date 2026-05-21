import chess
from search import getBestMove
from evaluation import evaluateBoard
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
board = chess.Board()
player_color = chess.WHITE  # Default: human plays White

SEARCH_DEPTH = 4


# --- Routes ---
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/fen")
def get_fen():
    return jsonify({
        "fen": board.fen(),
        "game_over": board.is_game_over(),
        "turn": "w" if board.turn else "b"
    })


@app.route("/move", methods=["POST"])
def make_move():
    data = request.get_json()
    source = data.get("source")
    target = data.get("target")
    promotion = data.get("promotion", "q")

    move_uci = source + target
    move = chess.Move.from_uci(move_uci)

    # If not legal, try with promotion
    if move not in board.legal_moves:
        move_uci_promo = move_uci + promotion
        move = chess.Move.from_uci(move_uci_promo)

    if move in board.legal_moves:
        board.push(move)
        
        #  BOT RESPONSE ---
        bot_move_uci = None
        bot_color = not player_color  # The bot plays the opposite color
        
        if board.turn == bot_color and not board.is_game_over():
            # searching algorithm
            bot_move_uci = getBestMove(board, SEARCH_DEPTH)
            if bot_move_uci is not None:
                bot_move = chess.Move.from_uci(bot_move_uci)
                board.push(bot_move)
        # ---

        return jsonify({
            "valid": True,
            "fen": board.fen(),
            "score": evaluateBoard(board),
            "game_over": board.is_game_over(),
            "turn": "w" if board.turn else "b",
            "is_check": board.is_check(),
            "result": board.result() if board.is_game_over() else None,
            "bot_move": bot_move_uci
        })
    else:
        return jsonify({
            "valid": False,
            "fen": board.fen(),
            "reason": "Illegal move!"
        })


@app.route("/reset", methods=["POST"])
def reset_board():
    global board, player_color
    
    # Parse the requested color from the frontend
    data = request.get_json() or {}
    color_req = data.get("player_color", "w")
    player_color = chess.WHITE if color_req == "w" else chess.BLACK
    
    board = chess.Board()
    
    # If the human chose Black, the bot (White) must make the first move
    bot_first_move = None
    if player_color == chess.BLACK and not board.is_game_over():
        bot_move_uci = getBestMove(board, SEARCH_DEPTH)
        if bot_move_uci:
            board.push(chess.Move.from_uci(bot_move_uci))
            bot_first_move = bot_move_uci

    return jsonify({
        "fen": board.fen(),
        "score": 0,
        "turn": "w" if board.turn else "b",
        "player_color": color_req,
        "bot_move": bot_first_move
    })


@app.route("/undo", methods=["POST"])
def undo_move():
    global board
    if len(board.move_stack) > 0:
        # Undo bot move + human move (2 half-moves)
        undone = 0
        while undone < 2 and len(board.move_stack) > 0:
            board.pop()
            undone += 1
        return jsonify({
            "valid": True,
            "fen": board.fen(),
            "turn": "w" if board.turn else "b",
            "undone": undone
        })
    else:
        return jsonify({
            "valid": False,
            "fen": board.fen(),
            "reason": "No moves to undo!"
        })


if __name__ == "__main__":
    print("♟ Chess Engine running at http://127.0.0.1:5000")
    app.run(debug=True)