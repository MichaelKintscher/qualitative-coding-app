from PySide6.QtWidgets import QWidget, QPushButton, QStyle, \
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit

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

        # Create the timestamp label.
        self.time_stamp = QLabel()
        self.time_stamp.setText("")

        # Create the forward backward button
        self.forward_button = QPushButton("Forward")
        self.backward_button = QPushButton("Backward")

        # Create empty widgets to fill negative space (remove later).
        empty_widget1 = QWidget()
        empty_widget2 = QWidget()

        # Create widgets for the user input
        self.timestamp_input = QLineEdit()
        self.go_to_timestamp_button = QPushButton("Go to timestamp")

        # Adds the widgets to the layout.
        horizontal_layout.addWidget(self.playback_speed_combo_box, stretch=3)
        horizontal_layout.addWidget(empty_widget1, stretch=3)
        horizontal_layout.addWidget(self.backward_button, stretch=2)
        horizontal_layout.addWidget(self.play_pause_button, stretch=1)
        horizontal_layout.addWidget(self.forward_button, stretch=2)
        horizontal_layout.addWidget(empty_widget2, stretch=4)
        horizontal_layout.addWidget(self.time_stamp, stretch=2)
        horizontal_layout.addWidget(self.timestamp_input)
        horizontal_layout.addWidget(self.go_to_timestamp_button)

        self.setLayout(horizontal_layout)
