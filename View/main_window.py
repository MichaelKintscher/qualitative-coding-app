from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QStyle, QHBoxLayout, QWidget, QVBoxLayout, QMessageBox

from View.coding_assistance_panel import CodingAssistancePanel
from View.media_panel import MediaPanel
from View.table_panel import TablePanel


class MainWindow(QMainWindow):
    """MainWindow is the main window of the application."""

    def __init__(self):
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

    def connect_load_video_to_slot(self, slot):
        """
        In this case this function checks whether the load video button is pressed
        then calls the slot specific slot function in the controller.

        Parameters:
            slot: The handler function that is called when the signal is clicked.
        """
        self._open_action.triggered.connect(slot)

    def connect_export_file_to_slot(self, slot):
        """
        In this case this function checks whether the Save table data button is pressed
        then calls the slot specific slot function in the controller.

        Parameters:
            slot: The handler function that is called when the signal is clicked.
        """
        self._save_action.triggered.connect(slot)

    def create_menu_bar(self):
        """
        Creates the main menu-bar for the application window and populates it with a
        File sub-menu and Export sub-menu.
        """
        file_menu = self.menuBar().addMenu("File")
        # Accesses image from the resource qrc file.
        file_dialog_icon = self.style().standardIcon(QStyle.SP_FileDialogStart)

        # Adds a load video button with an action.
        self._open_action = QAction(file_dialog_icon, "Load video file", self)
        file_menu.addAction(self._open_action)

        # This adds a new sub-menu for exporting a file.
        export_menu = self.menuBar().addMenu("Export")
        export_dialog_icon = self.style().standardIcon(QStyle.SP_DialogSaveButton)

        # Adds a Save table data button with an action.
        self._save_action = QAction(export_dialog_icon, "Save table data", self)
        export_menu.addAction(self._save_action)

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
        horizontal_layout.addWidget(self.media_panel, stretch=16)
        horizontal_layout.addWidget(self.coding_assistance_panel, stretch=5)
        top_container_widget.setLayout(horizontal_layout)

        vertical_container_layout.addWidget(top_container_widget, stretch=9)
        vertical_container_layout.addWidget(self.table_panel)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.centralWidget().setLayout(vertical_container_layout)
