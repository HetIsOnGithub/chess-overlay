import cv2


class BoardMapper:

    def draw_grid(self, frame):

        height, width = frame.shape[:2]

        square_w = width / 8
        square_h = height / 8

        files = "abcdefgh"

        # Grid Lines
        for col in range(9):

            x = int(col * square_w)

            cv2.line(
                frame,
                (x, 0),
                (x, height),
                (0, 255, 0),
                2
            )

        for row in range(9):

            y = int(row * square_h)

            cv2.line(
                frame,
                (0, y),
                (width, y),
                (0, 255, 0),
                2
            )

        # Chess Coordinates
        for row in range(8):

            for col in range(8):

                square = (
                    files[col]
                    + str(8 - row)
                )

                x = int(col * square_w + 5)
                y = int(row * square_h + 20)

                cv2.putText(
                    frame,
                    square,
                    (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 255),
                    1,
                    cv2.LINE_AA
                )

        return frame