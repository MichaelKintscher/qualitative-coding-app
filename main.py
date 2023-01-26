import sys

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QApplication

from Controllers.controller import Controller
from View.main_window import MainWindow
from View.start_dialog import StartDialog


def main():
    """Instantiates the qualitative coding desktop application."""
    # Initialize a global QSettings instance for data persistence.
    QCoreApplication.setOrganizationName("Capstone")
    QCoreApplication.setApplicationName("Qualitative-Coding-Desktop-Application")

    app = QApplication([])

    # Before displaying the main application window, load a "welcome"
    # window which allows the user to choose their session instance.
    start_dialog = StartDialog()
    dialog_choice = start_dialog.exec()



    # If the user rejected the start dialog box, then exit.
    if dialog_choice == 0:
        return

    # Session is chosen, load the main application.
    window = MainWindow(start_dialog.session_id)
    window.show()
    controller = Controller(window)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
