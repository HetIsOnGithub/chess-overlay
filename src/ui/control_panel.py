import json
import os
import cv2

from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QLineEdit
)

from PyQt6.QtCore import QTimer

from capture.screen_capture import ScreenCapture
from board.selector import BoardSelector
from board.board_mapper import BoardMapper
from board.square_extractor import SquareExtractor
from detection.occupancy_detector import OccupancyDetector
from detection.piece_detector import PieceDetector
from board.board_scanner import BoardScanner


class ControlPanel(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chess Overlay MVP")
        self.resize(450, 300)

        self.capture = ScreenCapture()
        self.selector = BoardSelector()
        self.mapper = BoardMapper()
        self.extractor = SquareExtractor()
        self.detector = OccupancyDetector()
        self.piece_detector = PieceDetector()
        self.board_scanner = BoardScanner()

        self.preview_running = False

        self.region = self.load_region()

        self.status_label = QLabel("Status: Ready")

        self.region_label = QLabel(
            self.region_text()
        )

        self.select_button = QPushButton(
            "Select Board Region"
        )

        self.preview_button = QPushButton(
            "Start Live Preview"
        )
        
        self.test_square_button = QPushButton(
            "Test Square e2"
        )
        
        self.scan_button = QPushButton(
            "Scan Board Occupancy"
        )
        
        self.detect_piece_button = QPushButton(
            "Detect e2 Piece"
        )
        
        self.square_input = QLineEdit()

        self.square_input.setText(
            "e2"
        )
        
        self.scan_pieces_button = QPushButton(
            "Scan All Pieces"
        )

        self.save_square_button = QPushButton(
            "Save Square"
        )
        
        self.scan_button.clicked.connect(
            self.scan_board
        )
        
        self.test_square_button.clicked.connect(
            self.test_square
        )
        
        self.save_square_button.clicked.connect(
            self.save_square
        )

        self.select_button.clicked.connect(
            self.select_board
        )
        
        self.detect_piece_button.clicked.connect(
            self.detect_piece
        )
        
        self.scan_pieces_button.clicked.connect(
            self.scan_pieces
        )

        self.preview_button.clicked.connect(
            self.toggle_preview
        )

        layout = QVBoxLayout()

        layout.addWidget(self.status_label)
        layout.addWidget(self.region_label)
        layout.addWidget(self.select_button)
        layout.addWidget(self.preview_button)
        layout.addWidget(self.test_square_button)
        layout.addWidget(self.scan_button)
        layout.addWidget(self.square_input)
        layout.addWidget(self.save_square_button)
        layout.addWidget(self.detect_piece_button)
        layout.addWidget(self.scan_pieces_button)

        self.setLayout(layout)

        self.timer = QTimer()

        self.timer.timeout.connect(
            self.update_preview
        )

    def region_text(self):

        return (
            f"X={self.region['left']} "
            f"Y={self.region['top']} "
            f"W={self.region['width']} "
            f"H={self.region['height']}"
        )

    def load_region(self):

        config_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "config.json"
        )

        config_path = os.path.abspath(
            config_path
        )

        if os.path.exists(config_path):

            with open(
                config_path,
                "r"
            ) as file:

                return json.load(file)

        return {
            "left": 0,
            "top": 0,
            "width": 0,
            "height": 0
        }

    def save_region(self):

        config_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "config.json"
        )

        config_path = os.path.abspath(
            config_path
        )

        with open(
            config_path,
            "w"
        ) as file:

            json.dump(
                self.region,
                file,
                indent=4
            )

    def select_board(self):

        self.status_label.setText(
            "Capturing screen..."
        )

        image = self.capture.capture_fullscreen()

        self.region = self.selector.select_region(
            image
        )

        self.save_region()

        self.region_label.setText(
            self.region_text()
        )

        self.status_label.setText(
            "Board selected"
        )

    def toggle_preview(self):

        if not self.preview_running:

            self.preview_running = True

            self.preview_button.setText(
                "Stop Live Preview"
            )

            self.timer.start(100)

        else:

            self.preview_running = False

            self.preview_button.setText(
                "Start Live Preview"
            )

            self.timer.stop()

            cv2.destroyAllWindows()

    def update_preview(self):

        if self.region["width"] == 0:
            return

        frame = self.capture.capture_region(
        self.region
    )

        frame = self.mapper.draw_grid(
        frame
    )

        cv2.imshow(
        "Board Preview",
        frame
    )

        cv2.waitKey(1)
        
    
    def test_square(self):

        if self.region["width"] == 0:
            return

        frame = self.capture.capture_region(
            self.region
    )

        square = self.extractor.get_square_image(
            frame,
            "e2"
    )

        cv2.imshow(
            "Square e2",
            square
    )

        cv2.waitKey(1)
        
    def scan_board(self):

        if self.region["width"] == 0:
            return

        frame = self.capture.capture_region(
            self.region
        )

        squares = self.extractor.get_all_squares(
            frame
        )

        print("\n========== BOARD ==========\n")

        for square_name, image in squares.items():

            occupied = self.detector.is_occupied(
                image
            )

            state = (
                "OCCUPIED"
                if occupied
                else "EMPTY"
            )

            print(
                f"{square_name} = {state}"
            )

        print(
            "\n===========================\n"
        )
        
    
    def save_square(self):

        if self.region["width"] == 0:
            return

        square_name = (
            self.square_input.text()
            .strip()
            .lower()
        )

        if len(square_name) != 2:

            self.status_label.setText(
                "Invalid square"
            )

            return

        frame = self.capture.capture_region(
            self.region
        )

        square = self.extractor.get_square_image(
            frame,
            square_name
        )

        debug_dir = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "debug"
        )

        debug_dir = os.path.abspath(
            debug_dir
        )

        os.makedirs(
            debug_dir,
            exist_ok=True
        )

        save_path = os.path.join(
            debug_dir,
            f"{square_name}.png"
        )

        cv2.imwrite(
            save_path,
            square
        )

        print(
            f"Saved: {save_path}"
        )

        self.status_label.setText(
            f"Saved {square_name}.png"
        )
        
    
    def detect_piece(self):

        if self.region["width"] == 0:
            return

        frame = self.capture.capture_region(
            self.region
        )

        square = self.extractor.get_square_image(
            frame,
            "a2"
        )

        piece, score = (
            self.piece_detector.detect_piece(
                square
            )
        )

        print()

        print(
            f"Detected: {piece}"
        )

        print(
            f"Score: {score:.4f}"
        )

        print()

        self.status_label.setText(
            f"{piece} ({score:.2f})"
        )
        
    
    def scan_pieces(self):

        if self.region["width"] == 0:
            return

        frame = self.capture.capture_region(
            self.region
        )

        board = (
            self.board_scanner.scan_board(
                frame,
                self.extractor,
                self.piece_detector
            )
        )

        print()

        print("===== BOARD =====")

        piece_count = 0

        for square, data in board.items():

            piece = data["piece"]

            if piece is None:
                continue

            piece_count += 1

            print(
                f"{square}: "
                f"{piece} "
                f"({data['score']:.2f})"
            )

        print()

        print(
            f"Detected pieces: {piece_count}"
        )

        print("=================")