from PySide6.QtMultimedia import QAudioOutput
from PySide6.QtWidgets import QWidget, QVBoxLayout

from View.media_control_panel import MediaControlPanel
from View.ScalableScrubbingBar.scalable_scrubber_bar import ScalableScrubberBar
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
        
        # Create sliders for the scalable scrubbing bars.
        self.scalable_scrubber_bar = ScalableScrubberBar()

        # Add vertical layout box to add widgets
        vertical_layout = QVBoxLayout()

        vertical_layout.setSpacing(0)
        vertical_layout.addWidget(self.video_widget, stretch=2)
        vertical_layout.addWidget(self.scalable_scrubber_bar, stretch=1)
        vertical_layout.addWidget(self.media_control_panel)
        self.setLayout(vertical_layout)
