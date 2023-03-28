from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QTransform
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSlider, QStackedLayout, QGridLayout, QHBoxLayout, QLabel
from superqt import QRangeSlider, QLabeledRangeSlider

from View.progress_bar_view import ProgressBarView
from View.scaling_bar import ScalingBar


class ScrubberBar(QWidget):
    """
    The ScrubbingBar is a custom widget, including a scaling bar and progress
    bars, that when combined, form a functional scalable scrubbing bar.
    """
    DEFAULT_RANGE_BOUNDS = (0, 100)
    DEFAULT_FPS = 30

    def __init__(self):
        """
        Constructs an instance of the scrubbing bar. The constructor creates
        the necessary components of the scrubbing bar and sets initial
        properties. It also sets the layout of the scrubbing bar widget.
        """
        super().__init__()

        # Compute the default frames per millisecond.
        self.frames_per_millisecond = 1 / (self.DEFAULT_FPS / 1000)

        self.scaling_bar = QLabeledRangeSlider(Qt.Orientation.Horizontal)
        self.scaling_bar.setEdgeLabelMode(QLabeledRangeSlider.LabelPosition.NoLabel)
        self.scaling_bar = ScalingBar()
        self.scaling_bar.setBarMovesAllHandles(True)
        self.scaling_bar.setRange(self.DEFAULT_RANGE_BOUNDS[0], self.DEFAULT_RANGE_BOUNDS[1])
        self.scaling_bar.setValue((self.DEFAULT_RANGE_BOUNDS[0], self.DEFAULT_RANGE_BOUNDS[1]))
        self.scaling_bar.setTickInterval(self.frames_per_millisecond)
        self.scaling_bar.setTickPosition(QSlider.TicksBelow)

        # This slider will be read-only, represents the progress for the scaling bar.
        self.scaling_progress_view = QSlider(Qt.Orientation.Horizontal)
        self.scaling_progress_view.setEnabled(False)
        self.scaling_progress_view.setTickInterval(self.frames_per_millisecond)
        self.scaling_progress_view.setTickPosition(QSlider.TicksBelow)

        self.progress_bar_view = ProgressBarView()

        progress_bar = self.get_progress_bar()
        progress_bar.setRange(self.DEFAULT_RANGE_BOUNDS[0], self.DEFAULT_RANGE_BOUNDS[1])
        progress_bar.setValue(self.DEFAULT_RANGE_BOUNDS[0])

        self.slider_max = self.DEFAULT_RANGE_BOUNDS[1]

        scaling_bar_horizontal_layout = QHBoxLayout()
        scaling_bar_label = QLabel("Scaling Bar")
        scaling_bar_label.setFixedWidth(90)
        scaling_bar_horizontal_layout.addWidget(scaling_bar_label)
        scaling_bar_horizontal_layout.addWidget(self.scaling_bar)

        scaling_progress_view_horizontal_layout = QHBoxLayout()
        scaling_progress_view_label = QLabel("Progress Bar")
        scaling_progress_view_label.setFixedWidth(90)
        scaling_progress_view_horizontal_layout.addWidget(scaling_progress_view_label)
        scaling_progress_view_horizontal_layout.addWidget(self.scaling_progress_view)

        progress_bar_horizontal_layout = QHBoxLayout()
        progress_bar_label = QLabel("Scrubber Bar")
        progress_bar_label.setFixedWidth(90)
        progress_bar_horizontal_layout.addWidget(progress_bar_label)
        progress_bar_horizontal_layout.addWidget(self.progress_bar_view)

        vertical_layout = QVBoxLayout()
        vertical_layout.addLayout(scaling_bar_horizontal_layout)
        vertical_layout.addLayout(scaling_progress_view_horizontal_layout)
        vertical_layout.addLayout(progress_bar_horizontal_layout)

        self.setLayout(vertical_layout)

    def initialize(self, upper_bound, fps):
        """
        Sets the range and values of the scrubbing bar. The scaling bar will
        always range from [0, upper_bound]. The progress bar will only
        initially range from [0, upper_bound]. This method should be called
        once the duration of the loaded video is known.

        Parameters:
            upper_bound - upper bound to set to the scrubbing bar.
            fps - frames per second
        """
        self.scaling_bar.setRange(0, upper_bound)
        self.scaling_bar.setValue((0, upper_bound))
        self.slider_max = upper_bound

        self.scaling_progress_view.setRange(0, upper_bound)

        progress_bar = self.get_progress_bar()
        progress_bar.setRange(0, upper_bound)
        progress_bar.setValue(0)

        self.frames_per_millisecond = 1 / (fps / 1000)
        self.scaling_bar.setTickInterval(self.frames_per_millisecond)
        self.scaling_progress_view.setTickInterval(self.frames_per_millisecond)
        self.get_progress_bar().setTickInterval(self.frames_per_millisecond)

        self.set_progress_zoom(0, upper_bound)

    def get_progress_bar(self):
        """
        Getter method that returns a reference to the progress bar.

        Return:
            reference to the progress bar
        """
        return self.progress_bar_view.get_progress_bar()

    def set_progress_zoom(self, lower_unit, upper_unit):
        """
        Scales and zooms the progress bar to reflect the range of the scaling
        bar. This method also changes the tick intervals according to the zoom
        level.

        Parameters:
            lower_unit - unit value (ms) of left handle of scaling bar
            upper_unit - unit value (ms) of right handle of scaling bar
        """
        w, h = self.get_progress_bar().width(), self.get_progress_bar().height()
        width_scale = (upper_unit - lower_unit) / self.slider_max
        mid_point = (lower_unit + (upper_unit - lower_unit) / 2) / self.slider_max
        self.progress_bar_view.setTransform(QTransform.fromScale(1 / width_scale, 1))
        self.progress_bar_view.centerOn(mid_point * w, self.get_progress_bar().height() / 2)

        if width_scale < 0.5:
            self.get_progress_bar().setTickInterval(self.frames_per_millisecond)
        else:
            self.get_progress_bar().setTickInterval(self.frames_per_millisecond * 2)
