import sys

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QApplication

from Controllers.state_controller import StateController


def main():
    """Instantiates the qualitative coding desktop application."""
    # Initialize a global QSettings instance for data persistence.
    QCoreApplication.setOrganizationName("Capstone")
    QCoreApplication.setApplicationName("Qualitative-Coding-Desktop-Application")

    app = QApplication([])

    state_controller = StateController()
    state_controller.exec_start()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
