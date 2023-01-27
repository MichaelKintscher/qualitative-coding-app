import PySide6
from PySide6.QtMultimedia import QAudioOutput
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSlider

from View.media_control_panel import MediaControlPanel
from View.video_widget import VideoWidget


class MediaPanel(QWidget):
    """
    Container of all Media player related widgets.
    """

    def __init__(self):
        """
        Constructor - Creates the related Media Player widgets and adds them
        to the panel using a QVBoxLayout.
        """
        super().__init__()

        self.video_widget = VideoWidget()
        self.audio_widget = QAudioOutput()
        self.media_control_panel = MediaControlPanel()
        
        # Create slider for the media player
        self.progress_bar_slider = QSlider(PySide6.QtCore.Qt.Orientation.Horizontal)
        
        # Add vertical layout box to add widgets
        vertical_layout = QVBoxLayout()

        vertical_layout.addWidget(self.video_widget, stretch=7)
        vertical_layout.addWidget(self.progress_bar_slider)

        vertical_layout.addWidget(self.media_control_panel)
        self.setLayout(vertical_layout)
