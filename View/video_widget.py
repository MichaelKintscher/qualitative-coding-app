from PySide6.QtCore import QSize
from PySide6.QtMultimediaWidgets import QVideoWidget


class VideoWidget(QVideoWidget):
    """
    Custom QVideoWidget which overrides QWidget functions to preserve a 16:9 aspect
    ratio.
    """
    def __init__(self):
        """
        Construct a Video Widget instance and set its size policy.
        """
        super().__init__()
        p = self.sizePolicy()
        p.setHeightForWidth(True)
        p.setWidthForHeight(True)
        self.setSizePolicy(p)

        self.minimum_width = 500

        # Set the minimum size.
        self.setMinimumWidth(self.minimum_width)
        self.setMinimumHeight(self.heightForWidth(self.minimum_width))

    def heightForWidth(self, width):
        """The video widget height should be 9/16 of the width."""
        return (9 / 16) * width

    def sizeHint(self):
        """Set the preferred sizing to follow the 16:9 aspect ratio."""
        w = self.width()
        return QSize(w, self.heightForWidth(w))
