import PySide6
from PySide6.QtGui import QPalette
from PySide6.QtMultimedia import QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSlider

from View.media_control_panel import MediaControlPanel


class MediaPanel(QWidget):
    """Container of all Media player related widgets."""

    def __init__(self):
        """
        Constructor - Creates the related Media Player widgets and adds them
        to the panel using a QVBoxLayout.
        """
        super().__init__()

        self.video_widget = QVideoWidget()
        self.audio_widget = QAudioOutput()
        self.progress_bar_placeholder = QSlider(PySide6.QtCore.Qt.Orientation.Horizontal)
        self.media_control_panel = MediaControlPanel()

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.video_widget, stretch=7)
        vertical_layout.addWidget(self.progress_bar_placeholder)
        vertical_layout.addWidget(self.media_control_panel)
        self.setLayout(vertical_layout)
