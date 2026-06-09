class SquareExtractor:

    def get_square_image(
        self,
        frame,
        square
    ):

        files = "abcdefgh"

        file_index = files.index(
            square[0]
        )

        rank = int(square[1])

        row = 8 - rank
        col = file_index

        height, width = frame.shape[:2]

        square_w = width // 8
        square_h = height // 8

        x1 = col * square_w
        y1 = row * square_h

        x2 = x1 + square_w
        y2 = y1 + square_h

        return frame[
            y1:y2,
            x1:x2
        ]

    def get_all_squares(
        self,
        frame
    ):

        squares = {}

        files = "abcdefgh"

        for rank in range(8, 0, -1):

            for file in files:

                square_name = (
                    file +
                    str(rank)
                )

                squares[
                    square_name
                ] = self.get_square_image(
                    frame,
                    square_name
                )

        return squares