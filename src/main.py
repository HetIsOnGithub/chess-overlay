import sys

from PyQt6.QtWidgets import QApplication
from ui.control_panel import ControlPanel


def main():
    app = QApplication(sys.argv)

    window = ControlPanel()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()