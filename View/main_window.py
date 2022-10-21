from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout


class MainWindow(QMainWindow):
    """MainWindow is the main window of the application."""

    def __init__(self):
        """
        Constructor - Initializes the properties of the main window.
        """
        super().__init__()

        self.setWindowTitle("Qualitative Coding Desktop App")
        self.setWindowState(Qt.WindowMaximized)

        central_widget = QWidget()

        horizontal_layout = QHBoxLayout()
        
        encoding_table_widget = EncodingTableWidget()
        horizontal_layout.addWidget(encoding_table_widget)
        
        self.setCentralWidget(central_widget)
        self.centralWidget().setLayout(horizontal_layout)

