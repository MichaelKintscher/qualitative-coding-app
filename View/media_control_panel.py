from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QBoxLayout, QSizePolicy


class MediaControlPanel(QWidget):
    """Container of all Media Control related widgets."""

    def __init__(self):
        """
        Constructor - Creates the related Media Control widgets and adds them
        to the panel using some layout.
        """
        super().__init__()
