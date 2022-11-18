from datetime import datetime

from PySide6.QtCore import Qt, QCoreApplication, QSettings
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QStyle, QHBoxLayout, QWidget, QVBoxLayout, QMessageBox

from View.coding_assistance_panel import CodingAssistancePanel
from View.media_panel import MediaPanel
from View.table_panel import TablePanel


class MainWindow(QMainWindow):
    """MainWindow is the main window of the application."""

    def __init__(self, session_id):
        """
        Constructor - Initializes the properties of the main window and all
        containing widgets.
        """
        super().__init__()

        self.setWindowTitle("Qualitative Coding Desktop App")
        self.setWindowState(Qt.WindowMaximized)

        self.create_menu_bar()

        self.table_panel = TablePanel()
        self.media_panel = MediaPanel()
        self.coding_assistance_panel = CodingAssistancePanel()

        self.set_layout()

        self.session_id = session_id
        if self.session_id != "New Session":
            self.read_settings()

    def closeEvent(self, event):
        """
        Event handler for the user closing the window.
        """
        self.write_settings()
        event.accept()

    def connect_load_video_to_slot(self, slot):
        """
        In this case this function checks whether the load video button is pressed
        then calls the slot specific slot function in the controller.

        Parameters:
            slot: The handler function that is called when the signal is clicked.
        """
        self._open_file_dialog_action.triggered.connect(slot)

    def connect_settings_to_slot(self, slot):
        """
        In this case this function checks whether the settings button is pressed
        then calls the slot specific slot function in the controller.

        Parameters:
            slot: The handler function that is called when the signal is clicked.
        """
        self._open_settings_dialog_action.triggered.connect(slot)

    def create_menu_bar(self):
        """
        Creates the main menu-bar for the application window and populates it with a
        File sub-menu, and a settings sub-menu.
        """
        file_menu = self.menuBar().addMenu("File")
        settings_menu = self.menuBar().addMenu("Settings")
        # Accesses image from the resource qrc file.
        file_dialog_icon = self.style().standardIcon(QStyle.SP_FileDialogStart)
        settings_dialog_icon = self.style().standardIcon(QStyle.SP_FileDialogDetailedView)
        # Adds a load video button with an action.
        self._open_file_dialog_action = QAction(file_dialog_icon, "Load video file", self)
        self._open_settings_dialog_action = QAction(settings_dialog_icon, "Settings", self)
        file_menu.addAction(self._open_file_dialog_action)
        settings_menu.addAction(self._open_settings_dialog_action)

    def read_settings(self):
        """
        Reads the QSettings object and restore state if it currently exists and if
        the user wants to reload the previous session.
        """
        self.table_panel.table.read_settings(self.session_id)

    def set_layout(self):
        """
        Sets the layout for the main window and adds the window's panels to
        the layout.
        """
        vertical_container_layout = QVBoxLayout()

        # Create a container widget for the video and coding assistance panels
        # to be stored in the first slot in the vertical container layout.
        top_container_widget = QWidget()
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(self.media_panel, stretch=3)
        horizontal_layout.addWidget(self.coding_assistance_panel, stretch=2)
        top_container_widget.setLayout(horizontal_layout)

        vertical_container_layout.addWidget(top_container_widget)
        vertical_container_layout.addWidget(self.table_panel)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.centralWidget().setLayout(vertical_container_layout)

    def write_settings(self):
        """
        Saves the state of the application to the QSettings object.
        """
        # If this session is new, save it as a new session group using the current time
        # as an identifier. Otherwise, use the previous identifier.
        if self.session_id == "New Session":
            self.session_id = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Create the group for this session and save the user data in it.
        self.table_panel.table.write_settings(self.session_id)
