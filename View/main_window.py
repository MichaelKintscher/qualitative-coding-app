from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QAction
from PySide6.QtMultimedia import QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import QMainWindow, QStyle, QHBoxLayout, QWidget

from View.encoding_table_widget import EncodingTableWidget


class MainWindow(QMainWindow):
    """MainWindow is the main window of the application."""

    def __init__(self):
        """
        Constructor - Initializes the properties of the main window and all
        containing GUI elements.
        """
        super().__init__()

        self.setWindowTitle("Qualitative Coding Desktop App")
        self.setWindowState(Qt.WindowMaximized)

        self.create_menu_bar()

        self._video_widget = QVideoWidget()
        self._audio_widget = QAudioOutput()
        self._encoding_table_widget = EncodingTableWidget()

        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(self._video_widget, stretch=1)
        horizontal_layout.addWidget(self._encoding_table_widget, stretch=1)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.centralWidget().setLayout(horizontal_layout)

    def get_encoding_table_widget(self):
        return self._encoding_table_widget

    def connect_load_video_to_slot(self, slot):
        """
        In this case this function checks whether the load video button is pressed
        then calls the slot specific slot function in the controller.

        Parameters:
            slot: The handler function that is called when the signal is clicked.
        """
        self._open_action.triggered.connect(slot)

    def create_menu_bar(self):
        """
        Creates the main menu-bar for the application window and populates it with a
        File sub-menu.
        """
        file_menu = self.menuBar().addMenu("File")
        # Accesses image from the resource qrc file.
        file_dialog_icon = self.style().standardIcon(QStyle.SP_FileDialogStart)

        # Adds a load video button with an action.
        self._open_action = QAction(file_dialog_icon, "Load video file", self)
        file_menu.addAction(self._open_action)

    def get_audio_widget(self):
        """
        Gets the audio widget reference of the View.

        Return:
            Reference to the audio output widget.
        """
        return self._audio_widget

    def get_video_widget(self):
        """
        Gets the video widget reference of the View.

        Return:
            Reference to the video widget.
        """
        return self._video_widget
