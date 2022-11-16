from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QPushButton, QStyle, \
    QVBoxLayout, QHBoxLayout


class MediaControlPanel(QWidget):
    """ Container of all Media Control related widgets."""

    def __init__(self):
        """
        Constructor - Creates the related Media Control widgets and adds them
        to the panel using some layout.
        """
        super().__init__()
        
        # Create play pause butto n.
        self.play_pause_button = QPushButton()
        self.play_pause_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        
        # Create horizontal box layout.
        horizontal_layout = QHBoxLayout()
        horizontal_layout.setContentsMargins(0, 0, 0, 0)
        horizontal_layout.addWidget(self.play_pause_button)

        # Add vertical box layout to add all widgets.
        vboxLayout = QVBoxLayout()
        vboxLayout.addLayout(horizontal_layout)

        self.setLayout(vboxLayout)
