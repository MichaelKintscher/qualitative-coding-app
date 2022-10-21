import sys

from PySide6.QtWidgets import QApplication

from Controllers.controller import Controller
from View.main_window import MainWindow


def main():
    """Instantiates the qualitative coding desktop application."""
    app = QApplication([])
    window = MainWindow()
    window.show()
    controller = Controller(window)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
