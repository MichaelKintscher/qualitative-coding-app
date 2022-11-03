from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QBoxLayout, QSizePolicy, QHBoxLayout


class MediaControlPanel(QWidget):
    """Container of all Media Control related widgets."""

    def __init__(self):
        """
        Constructor - Creates the related Media Control widgets and adds them
        to the panel using some layout.
        """
        super().__init__()

        # Create an HBox layout and adds the items
        horizontal_layout = QHBoxLayout()

        self.time_stamp = QLabel()
        self.time_stamp.setText("")
        horizontal_layout.addWidget(self.time_stamp)

        self.setLayout(horizontal_layout)
