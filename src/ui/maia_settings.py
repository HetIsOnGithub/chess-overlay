import json
import os

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QComboBox
)


class MaiaSettings(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Maia Settings")
        self.resize(300, 200)

        layout = QVBoxLayout()

        layout.addWidget(
            QLabel("Maia ELO")
        )

        self.elo = QComboBox()

        for rating in range(
            700,
            2100,
            100
        ):
            self.elo.addItem(
                str(rating)
            )

        layout.addWidget(
            self.elo
        )

        layout.addWidget(
            QLabel("Play Side")
        )

        self.side = QComboBox()

        self.side.addItems(
            [
                "white",
                "black"
            ]
        )

        layout.addWidget(
            self.side
        )

        save_button = QPushButton(
            "Save"
        )

        save_button.clicked.connect(
            self.save_settings
        )

        layout.addWidget(
            save_button
        )

        self.setLayout(
            layout
        )

        self.load_settings()

    def config_path(self):

        return os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "config_maia.json"
            )
        )

    def load_settings(self):

        path = self.config_path()

        if not os.path.exists(path):
            return

        with open(
            path,
            "r"
        ) as file:

            data = json.load(file)

        self.elo.setCurrentText(
            str(
                data.get(
                    "elo",
                    700
                )
            )
        )

        self.side.setCurrentText(
            data.get(
                "side",
                "white"
            )
        )

    def save_settings(self):

        path = self.config_path()

        data = {
            "elo": int(
                self.elo.currentText()
            ),
            "side": (
                self.side.currentText()
            )
        }

        with open(
            path,
            "w"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

        print(
            "Saved:",
            data
        )


if __name__ == "__main__":

    app = QApplication([])

    window = MaiaSettings()

    window.show()

    app.exec()