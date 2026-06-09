import chess
import chess.engine

LC0_PATH = r"D:\PC_Exe\chess-overlay\engines\maia\lc0.exe"

MAIA_MODEL = r"D:\PC_Exe\chess-overlay\engines\maia\maia-1100.pb.gz"

engine = chess.engine.SimpleEngine.popen_uci(
    [
        LC0_PATH,
        "--weights=" + MAIA_MODEL
    ]
)

board = chess.Board()

result = engine.play(
    board,
    chess.engine.Limit(
        nodes=500
    )
)

print()
print("Maia move:")
print(result.move)
print()

engine.quit()