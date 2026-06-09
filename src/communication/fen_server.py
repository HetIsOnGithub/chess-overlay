from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS

import chess
import chess.engine
import json
import os

STOCKFISH_PATH = (
    r"D:\PC_Exe\Chess\maiai and stockfish both working\final working backiup\weowkeowewpod\chess-overlay\engines\stockfish.exe"
)

CONFIG_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "config_maia.json"
    )
)


app = Flask(__name__)
CORS(app)


current_elo = None
maia = None



def load_maia_settings():

    config_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "config_maia.json"
        )
    )

    with open(
        config_path,
        "r"
    ) as file:

        return json.load(file)

@app.route("/fen", methods=["POST"])
def receive_fen():

    data = request.json

    fen = data["fen"]
    

    settings = load_maia_settings()

    human_level = settings["elo"]

    selected_side = settings["side"]
    
    turn = "w" if selected_side == "white" else "b"

    board = chess.Board(
    f"{fen} {turn} - - 0 1"
)

    print()
    print("MAIA ELO:", human_level)
    print("SELECTED SIDE:", selected_side)
    print()

    global maia
    global current_elo

    if maia is None or current_elo != human_level:

        if maia:
            maia.quit()

        maia = chess.engine.SimpleEngine.popen_uci(
            [
                "maia3-uci",
                "--model",
                "maia3-5m",
                "--elo",
                str(human_level)
            ]
        )

    current_elo = human_level
    
    print()
    print("MAIA ELO:", human_level)
    print("SELECTED SIDE:", selected_side)
    print()
    

    stockfish = chess.engine.SimpleEngine.popen_uci(
    STOCKFISH_PATH
)

    stockfish_result = stockfish.play(
            board,
            chess.engine.Limit(
                depth=12
            )
        )

    maia_result = maia.play(
            board,
            chess.engine.Limit(
                nodes=500
            )
        )

    stockfish_move = str(
            stockfish_result.move
        )

    maia_move = str(
            maia_result.move
        )
    
    stockfish.quit()

    print()
    print("Stockfish:", stockfish_move)
    print("Maia:", maia_move)
    print()

    return jsonify(
            {
                "stockfish_move": stockfish_move,
                "maia_move": maia_move
            }
        )


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000
    )