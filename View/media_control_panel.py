from PySide6.QtWidgets import QWidget, QHBoxLayout

from View.playback_speed_combobox import PlaybackSpeedComboBox


class MediaControlPanel(QWidget):
    """Container of all Media Control related widgets."""

    def __init__(self):
        """
        Constructor - Creates the related Media Control widgets and adds them
        to the panel using a horizontal layout.
        """
        super().__init__()

        horizontal_layout = QHBoxLayout()

        # Create a playback speed combobox as a media control widget.
        self.playback_speed_combobox = PlaybackSpeedComboBox()

        # Create an empty widget to fill negative space (remove later).
        empty_widget = QWidget()

        # Adds the widgets to the layout.
        horizontal_layout.addWidget(self.playback_speed_combobox, stretch=1)
        horizontal_layout.addWidget(empty_widget, stretch=5)

        self.setLayout(horizontal_layout)
