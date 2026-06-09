function clearHighlights() {
  document
    .querySelectorAll(".chess-overlay-square")
    .forEach((el) => el.remove());
}

function highlightSquare(square, color) {
  const board = document.querySelector(".board");

  if (!board) {
    console.log("Board not found");
    return;
  }

  board.style.position = "relative";

  const cell = board.clientWidth / 8;

  
  const div = document.createElement("div");

  div.className = "chess-overlay-square";

  div.style.position = "absolute";
  div.style.pointerEvents = "none";

  const file = square.charCodeAt(0) - 97;
  const rank = parseInt(square[1]);

  const flipped = document
    .querySelector(".board")
    ?.classList.contains("flipped");

  if (flipped) {
    div.style.left = `${(7 - file) * cell}px`;
    div.style.top = `${(rank - 1) * cell}px`;
  } else {
    div.style.left = `${file * cell}px`;
    div.style.top = `${(8 - rank) * cell}px`;
  }

  div.style.width = `${cell}px`;
  div.style.height = `${cell}px`;

  div.style.backgroundColor = color;
  div.style.opacity = "0.5";

  div.style.zIndex = "999999";

  board.appendChild(div);
}

function showBestMove(stockfishMove, maiaMove) {
  clearHighlights();

  highlightSquare(stockfishMove.substring(0, 2), "#ff3333");

  highlightSquare(stockfishMove.substring(2, 4), "#ff3333");

  highlightSquare(maiaMove.substring(0, 2), "#9933ff");

  highlightSquare(maiaMove.substring(2, 4), "#9933ff");
}
