from PySide6.QtCore import Qt
from PySide6.QtGui import QTransform
from PySide6.QtWidgets import QSlider, QGraphicsView, QGraphicsScene, QSizePolicy


class ProgressBarView(QGraphicsView):
    """
    The ProgressBarView is a QGraphicsView object, painting a QSlider bar in a
    QGraphicsScene. The QSlider is resized to be an equivalent size as the
    scaling bar in the ScrubberBar class, as the ProgressBar is a component
    in the ScrubberBar. We utilize the Qt Graphics framework in order to
    "zoom in" to the progress bar, a feature useful for implementing the
    functionality of the scaling bar.
    """

    def __init__(self):
        """
        Constructs the QGraphicsView, initializing the progress bar and
        setting its width equal to the width of the graphics view.
        """
        self.scene = QGraphicsScene()
        self.progress_bar = QSlider(Qt.Orientation.Horizontal)
        self.progress_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.scene.addWidget(self.progress_bar)

        super().__init__(self.scene)
        self.progress_bar.setFixedWidth(self.width())
        self.setStyleSheet("border: 0px")
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def get_progress_bar(self):
        """
        Getter method that returns a reference to the progress bar.

        Return:
            reference to the progress bar
        """
        return self.progress_bar

    def resizeEvent(self, event):
        """
        Overrides the resizeEvent function in QGraphicsView, adding
        functionality on top to resize the progress bar in the scene
        to the width of the new graphics view widget.

        Parameters:
            event - resize event
        """
        super().resizeEvent(event)
        self.progress_bar.setFixedWidth(self.width())
        self.scene.setSceneRect(self.contentsRect())
        self.setFixedHeight(self.progress_bar.height())
