from PySide6.QtCore import Qt
from PySide6.QtGui import QTransform, QFontMetrics
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSlider, QHBoxLayout, QLabel

from View.progress_bar_view import ProgressBarView
from View.scaling_bar import ScalingBar


class ScrubberBar(QWidget):
    """
    The ScrubbingBar is a custom widget, including a scaling bar and progress
    bars, that when combined, form a functional scalable scrubbing bar.
    """
    DEFAULT_RANGE_BOUNDS = (0, 100)

    def __init__(self):
        """
        Constructs an instance of the scrubbing bar. The constructor creates
        the necessary components of the scrubbing bar and sets initial
        properties. It also sets the layout of the scrubbing bar widget.
        """
        super().__init__()

        # Since the timestamp label width will vary depending on font, we
        # compute the maximum width required to represent all timestamp labels.
        timestamp_width = self._compute_max_timestamp_width()
        horizontal_margin = timestamp_width // 2

        # Create and configure the scaling bar.
        self.scaling_bar_widget = ScalingBar(timestamp_width)
        self.scaling_bar = self.scaling_bar_widget.get_slider()
        self.scaling_bar.setBarMovesAllHandles(True)
        self.scaling_bar.setRange(self.DEFAULT_RANGE_BOUNDS[0], self.DEFAULT_RANGE_BOUNDS[1])
        self.scaling_bar.setValue((self.DEFAULT_RANGE_BOUNDS[0], self.DEFAULT_RANGE_BOUNDS[1]))

        # Add a label and the scaling bar to a layout.
        scaling_bar_horizontal_layout = QHBoxLayout()
        scaling_bar_label = QLabel("Scaling Bar")
        scaling_bar_label.setFixedWidth(90)
        scaling_bar_vertical_layout = QVBoxLayout()
        scaling_bar_vertical_layout.addWidget(self.scaling_bar_widget)
        scaling_bar_horizontal_layout.addWidget(scaling_bar_label)
        scaling_bar_horizontal_layout.addLayout(scaling_bar_vertical_layout)

        # Create and configure the progress bar (read only).
        self.scaling_progress_view = QSlider(Qt.Orientation.Horizontal)
        self.scaling_progress_view.setEnabled(False)

        # Add a label and the progress bar to a layout
        scaling_progress_view_horizontal_layout = QHBoxLayout()
        scaling_progress_view_label = QLabel("Progress Bar")
        scaling_progress_view_label.setFixedWidth(90)
        scaling_progress_view_layout_vertical = QVBoxLayout()
        scaling_progress_view_layout_vertical.setContentsMargins(horizontal_margin, 0, horizontal_margin, 0)
        scaling_progress_view_layout_vertical.addWidget(self.scaling_progress_view)
        scaling_progress_view_horizontal_layout.addWidget(scaling_progress_view_label)
        scaling_progress_view_horizontal_layout.addLayout(scaling_progress_view_layout_vertical)

        # Create and configure the scrubber bar
        self.progress_bar_view = ProgressBarView()
        progress_bar = self.get_progress_bar()
        progress_bar.setRange(self.DEFAULT_RANGE_BOUNDS[0], self.DEFAULT_RANGE_BOUNDS[1])
        progress_bar.setValue(self.DEFAULT_RANGE_BOUNDS[0])
        self.slider_max = self.DEFAULT_RANGE_BOUNDS[1]

        # Add a label and the scrubber bar to a layout
        progress_bar_horizontal_layout = QHBoxLayout()
        progress_bar_label = QLabel("Scrubber Bar")
        progress_bar_label.setFixedWidth(90)
        progress_bar_vertical_layout = QVBoxLayout()
        progress_bar_vertical_layout.setContentsMargins(horizontal_margin, 0, horizontal_margin, 0)
        progress_bar_vertical_layout.addWidget(self.progress_bar_view)
        progress_bar_horizontal_layout.addWidget(progress_bar_label)
        progress_bar_horizontal_layout.addLayout(progress_bar_vertical_layout)

        # Add all three bars to this widget's vertical layout
        vertical_layout = QVBoxLayout()
        vertical_layout.addLayout(scaling_bar_horizontal_layout)
        vertical_layout.addLayout(scaling_progress_view_horizontal_layout)
        vertical_layout.addLayout(progress_bar_horizontal_layout)
        self.setLayout(vertical_layout)

    def initialize(self, upper_bound):
        """
        Sets the range and values of the scrubbing bar. The scaling bar will
        always range from [0, upper_bound]. The progress bar will only
        initially range from [0, upper_bound]. This method should be called
        once the duration of the loaded video is known.

        Parameters:
            upper_bound - upper bound to set to the scrubbing bar.
        """
        self.scaling_bar.setRange(0, upper_bound)
        self.scaling_bar.setValue((0, upper_bound))
        self.slider_max = upper_bound

        self.scaling_progress_view.setRange(0, upper_bound)

        progress_bar = self.get_progress_bar()
        progress_bar.setRange(0, upper_bound)
        progress_bar.setValue(0)

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
        bar.

        Parameters:
            lower_unit - unit value (ms) of left handle of scaling bar
            upper_unit - unit value (ms) of right handle of scaling bar
        """
        w, h = self.get_progress_bar().width(), self.get_progress_bar().height()
        width_scale = (upper_unit - lower_unit) / self.slider_max
        mid_point = (lower_unit + (upper_unit - lower_unit) / 2) / self.slider_max
        self.progress_bar_view.setTransform(QTransform.fromScale(1 / width_scale, 1))
        self.progress_bar_view.centerOn(mid_point * w, self.get_progress_bar().height() / 2)

    def _compute_max_timestamp_width(self):
        """
        Computes the maximum timestamp width required to paint any arbitrary
        timestamp. The width of a timestamp will depend on the font used by
        the system.
        """
        max_width = 0
        font_metrics = QFontMetrics(self.font())

        # Some digits are wider than other digits.
        for digit in range(10):
            timestamp_with_digit_only = f"{digit}{digit}:{digit}{digit}:{digit}{digit}.{digit}{digit}"
            max_width = max(max_width, font_metrics.horizontalAdvance(timestamp_with_digit_only))

        return max_width
