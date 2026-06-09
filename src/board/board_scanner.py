class BoardScanner:

    def scan_board(
        self,
        frame,
        extractor,
        detector
    ):

        board = {}

        files = "abcdefgh"

        for rank in range(8, 0, -1):

            for file in files:

                square = (
                    file +
                    str(rank)
                )

                image = (
                    extractor.get_square_image(
                        frame,
                        square
                    )
                )

                piece, score = (
                    detector.detect_piece(
                        image
                    )
                )

                board[square] = {
                    "piece": piece,
                    "score": score
                }

        return board