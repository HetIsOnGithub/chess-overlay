import chess
import chess.engine


ENGINE_PATH = (
    r"D:\PC_Exe\chess-overlay\engines\stockfish.exe"
)


board = chess.Board()

engine = chess.engine.SimpleEngine.popen_uci(
    ENGINE_PATH
)

result = engine.play(
    board,
    chess.engine.Limit(
        depth=12
    )
)

print()
print("Best move:")
print(result.move)
print()

engine.quit()