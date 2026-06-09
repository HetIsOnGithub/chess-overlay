function squareToChess(squareClass) {
  const num = squareClass.replace("square-", "");

  const file = parseInt(num[0]);

  const rank = parseInt(num[1]);

  const files = "abcdefgh";

  return files[file - 1] + rank;
}

function pieceToFen(piece) {
  const map = {
    wp: "P",
    wn: "N",
    wb: "B",
    wr: "R",
    wq: "Q",
    wk: "K",

    bp: "p",
    bn: "n",
    bb: "b",
    br: "r",
    bq: "q",
    bk: "k",
  };

  return map[piece];
}

function buildFen(board) {
  let rows = [];

  for (let rank = 8; rank >= 1; rank--) {
    let row = "";
    let empty = 0;

    for (let file of "abcdefgh") {
      const square = file + rank;

      const piece = board[square];

      if (!piece) {
        empty++;
      } else {
        if (empty > 0) {
          row += empty;
          empty = 0;
        }

        row += pieceToFen(piece);
      }
    }

    if (empty > 0) {
      row += empty;
    }

    rows.push(row);
  }

  return rows.join("/");
}

let lastFen = "";

async function scanBoard() {
  const pieces = document.querySelectorAll(".piece");

  const board = {};

  pieces.forEach((piece) => {
    const classes = [...piece.classList];

    const pieceCode = classes.find((c) => c.length === 2);

    const squareClass = classes.find((c) => c.startsWith("square-"));

    const square = squareToChess(squareClass);

    board[square] = pieceCode;
  });

  const fen = buildFen(board);

  if (fen === lastFen) {
    return;
  }

  lastFen = fen;

  try {

    chrome.runtime.sendMessage(
      {
        type: "fen",
        fen: fen,

      },

      function (data) {
        console.clear();

        console.log("FEN:", fen);

        console.log("Response:", data);

        showBestMove(data.stockfish_move, data.maia_move);
      },
    );
  } catch (error) {
    console.error(error);
  }
}

setInterval(scanBoard, 1000);
