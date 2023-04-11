from PySide6.QtCore import Qt
from PySide6.QtGui import QFontMetrics
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSlider, QHBoxLayout, QLabel

from View.ScalableScrubbingBar.labeled_slider_tick_marks import LabeledSliderTickMarks
from View.ScalableScrubbingBar.scaling_bar import ScalingBar
from View.ScalableScrubbingBar.scrubber_bar import ScrubberBar


class ScalableScrubberBar(QWidget):
    """
    The ScalableScrubberBar is a custom widget, including a scaling bar and progress
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
        timestamp_width += 1 if timestamp_width % 2 == 1 else 0
        horizontal_margin = timestamp_width // 2

        # Create and configure the scaling bar.
        self.scaling_bar_widget = ScalingBar(timestamp_width)
        self.scaling_bar = self.scaling_bar_widget.get_slider()
        self.scaling_bar.setBarMovesAllHandles(True)
        self.scaling_bar.setRange(self.DEFAULT_RANGE_BOUNDS[0], self.DEFAULT_RANGE_BOUNDS[1])
        self.scaling_bar.setValue((self.DEFAULT_RANGE_BOUNDS[0], self.DEFAULT_RANGE_BOUNDS[1]))
        self.scaling_bar_tick_marks = LabeledSliderTickMarks(self.scaling_bar, timestamp_width)

        # Add a label and the scaling bar to a layout.
        scaling_bar_horizontal_layout = QHBoxLayout()
        scaling_bar_label = QLabel("Scaling Bar")
        scaling_bar_label.setFixedWidth(90)
        scaling_bar_vertical_layout = QVBoxLayout()
        scaling_bar_vertical_layout.setSpacing(0)
        scaling_bar_vertical_layout.addWidget(self.scaling_bar_widget)
        scaling_bar_vertical_layout.addWidget(self.scaling_bar_tick_marks)
        scaling_bar_horizontal_layout.addWidget(scaling_bar_label)
        scaling_bar_horizontal_layout.addLayout(scaling_bar_vertical_layout)

        # Create and configure the progress bar (read only).
        self.progress_bar = QSlider(Qt.Orientation.Horizontal)
        self.progress_bar.setEnabled(False)
        self.progress_bar_tick_marks = LabeledSliderTickMarks(self.progress_bar, timestamp_width)

        # Add a label and the progress bar to a layout
        progress_bar_horizontal_layout = QHBoxLayout()
        progress_bar_label = QLabel("Progress Bar")
        progress_bar_label.setFixedWidth(90)
        progress_bar_layout_vertical = QVBoxLayout()
        progress_bar_layout_vertical.setSpacing(0)
        progress_bar_inner_layout = QVBoxLayout()
        progress_bar_inner_layout.setContentsMargins(horizontal_margin, 0, horizontal_margin, 0)
        progress_bar_inner_layout.addWidget(self.progress_bar)
        progress_bar_layout_vertical.addLayout(progress_bar_inner_layout)
        progress_bar_layout_vertical.addWidget(self.progress_bar_tick_marks)
        progress_bar_horizontal_layout.addWidget(progress_bar_label)
        progress_bar_horizontal_layout.addLayout(progress_bar_layout_vertical)

        # Create and configure the scrubber bar
        self.scrubber_bar = ScrubberBar(self.scaling_bar)
        self.scrubber_bar.setRange(self.DEFAULT_RANGE_BOUNDS[0], self.DEFAULT_RANGE_BOUNDS[1])
        self.scrubber_bar.setValue(self.DEFAULT_RANGE_BOUNDS[0])
        self.slider_max = self.DEFAULT_RANGE_BOUNDS[1]
        self.scrubber_bar_tick_marks = LabeledSliderTickMarks(self.scrubber_bar, timestamp_width)

        # Add a label and the scrubber bar to a layout
        scrubber_bar_horizontal_layout = QHBoxLayout()
        scrubber_bar_label = QLabel("Scrubber Bar")
        scrubber_bar_label.setFixedWidth(90)
        scrubber_bar_vertical_layout = QVBoxLayout()
        scrubber_bar_vertical_layout.setSpacing(0)
        scrubber_bar_inner_layout = QVBoxLayout()
        scrubber_bar_inner_layout.setContentsMargins(horizontal_margin, 0, horizontal_margin, 0)
        scrubber_bar_inner_layout.addWidget(self.scrubber_bar)
        scrubber_bar_vertical_layout.addLayout(scrubber_bar_inner_layout)
        scrubber_bar_vertical_layout.addWidget(self.scrubber_bar_tick_marks)
        scrubber_bar_horizontal_layout.addWidget(scrubber_bar_label)
        scrubber_bar_horizontal_layout.addLayout(scrubber_bar_vertical_layout)

        # Add all three bars to this widget's vertical layout
        vertical_layout = QVBoxLayout()
        vertical_layout.addLayout(scaling_bar_horizontal_layout)
        vertical_layout.addLayout(progress_bar_horizontal_layout)
        vertical_layout.addLayout(scrubber_bar_horizontal_layout)
        self.setLayout(vertical_layout)

        # Hide the tick-mark bars until a video is loaded.
        self.scaling_bar_tick_marks.hide()
        self.progress_bar_tick_marks.hide()
        self.scrubber_bar_tick_marks.hide()

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

        self.progress_bar.setRange(0, upper_bound)
        self.scrubber_bar.setRange(0, upper_bound)

        # Display the tick-mark bars
        self.scaling_bar_tick_marks.show()
        self.progress_bar_tick_marks.show()
        self.scrubber_bar_tick_marks.show()

    def _compute_max_timestamp_width(self):
        """
        Computes the maximum timestamp width required to paint any arbitrary
        timestamp. The width of a timestamp will depend on the font used by
        the system.
        """
        max_width = 0
        font = self.font()
        font.setPointSize(10)
        font_metrics = QFontMetrics(font)

        # Some digits are wider than other digits.
        for digit in range(10):
            timestamp_with_digit_only = f"{digit}{digit}:{digit}{digit}:{digit}{digit}.{digit}{digit}"
            max_width = max(max_width, font_metrics.horizontalAdvance(timestamp_with_digit_only))

        return max_width
