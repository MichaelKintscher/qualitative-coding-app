from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QPushButton, QStyle, \
    QVBoxLayout, QHBoxLayout

from View.playback_speed_combo_box import PlaybackSpeedComboBox


class MediaControlPanel(QWidget):
    """ Container of all Media Control related widgets."""

    def __init__(self):
        """
        Constructor - Creates the related Media Control widgets and adds them
        to the panel using a horizontal layout.
        """
        super().__init__()
        
        # Create play pause button.
        self.play_pause_button = QPushButton()
        self.play_pause_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        
        # Create a playback speed combobox as a media control widget.
        self.playback_speed_combo_box = PlaybackSpeedComboBox()
        
        # Create horizontal box layout.
        horizontal_layout = QHBoxLayout()
        horizontal_layout.setContentsMargins(0, 0, 0, 0)
        horizontal_layout.addWidget(self.playback_speed_combo_box)
        horizontal_layout.addWidget(self.play_pause_button)

        # Add vertical box layout to add all widgets.
        vertical_layout = VBoxLayout()
        vertical_layout.addLayout(horizontal_layout)

        self.setLayout(vertical_layout)
