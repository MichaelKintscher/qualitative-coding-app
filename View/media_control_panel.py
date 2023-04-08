from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QPushButton, QStyle, \
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSizePolicy

from View.playback_speed_combo_box import PlaybackSpeedComboBox


class MediaControlPanel(QWidget):
    """ Container of all Media Control related widgets."""

    def __init__(self):
        """
        Constructor - Creates the related Media Control widgets and adds them
        to the panel using a horizontal layout.
        """
        super().__init__()

        # Create horizontal box layout.
        horizontal_layout = QHBoxLayout()

        # Create a playback speed combobox.
        self.playback_speed_combo_box = PlaybackSpeedComboBox()

        # Create play pause button.
        self.play_pause_button = QPushButton()
        self.play_pause_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_pause_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # Create the timestamp label.
        self.time_stamp = QLabel()
        self.time_stamp.setText("00:00:00/00:00:00")

        # Create empty widgets to fill negative space (remove later).
        empty_widget1 = QWidget()
        empty_widget2 = QWidget()
        empty_widget3 = QWidget()

        # Adds the widgets to the layout.
        horizontal_layout.addWidget(self.playback_speed_combo_box)
        horizontal_layout.addStretch()
        horizontal_layout.addWidget(self.play_pause_button)
        horizontal_layout.addStretch()
        horizontal_layout.addWidget(self.time_stamp)

        self.setLayout(horizontal_layout)
