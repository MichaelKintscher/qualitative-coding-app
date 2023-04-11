from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsScene, QGraphicsView


def _get_timestamp(time_ms):
    """
    Converts the given time, in milliseconds, to a timestamp string.

    Parameters:
        time_ms - time in milliseconds to convert.
    """
    centi_seconds = int((time_ms / 10) % 100)
    seconds = int((time_ms / 1000) % 60)
    minutes = int((time_ms / (1000 * 60)) % 60)
    hours = int((time_ms / (1000 * 60 * 60)) % 24)

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{centi_seconds:02d}"


class LabeledSliderTickMarks(QGraphicsView):
    """
    Custom widget that draws tick marks with timestamp labels for the provided
    slider. This widget should be placed directly below the slider.

    The Labeled Slider Tick Marks class uses the QT Graphics framework to draw
    tick marks and timestamps according to the range and zoom level of the given
    slider.

    {Note: This assumes that a certain positioning of the slider and tick mark
     bar, mainly that the bars are vertically aligned, and that the slider has
     a left and right content margin of 1/2 * label_width. And, the tick  mark
     bar has no margins.}
    """

    def __init__(self, slider, label_width):
        """
        Constructs an instance of the labeled slider tick marks widget.

        Parameters:
            slider - the slider to draw tick marks for.
            label_width - the width required to draw a timestamp label.
        """
        self._graphics_scene = QGraphicsScene()
        super().__init__(self._graphics_scene)

        self._label_width = label_width
        self._slider = slider
        self._slider.rangeChanged.connect(self._reposition_tick_marks)

        # Configure the graphics view visual characteristics.
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.setFrameStyle(0)
        self.setFixedHeight(35)

        # Hard coded tick intervals, one of which is chosen for the tick marks.
        self.tick_intervals_sec = [0.25, 0.50, 1, 1.5, 2, 5, 10, 30, 60, 120, 300, 600, 1800, 3600]

        # The slider handle is factored in the pixel computation of its width (estimated guess)
        self._slider_handle_width = self._slider.minimumSizeHint().width()
        self._slider_handle_offset = self._slider_handle_width // 2

        self._label_padding = 5
        self.setStyleSheet("background: transparent;")

    def _reposition_tick_marks(self):
        """
        Repositions the tick marks, dynamically choosing the best tick mark interval which
        maximizes the total number of tick marks displayed to give the user more information.
        """
        # Once again, this assumes the slider has a margin of 1/2 * label_width.
        start_slider_px = self._label_width // 2 + self._slider_handle_offset
        end_slider_px = self.width() - self._label_width // 2 - self._slider_handle_offset - 1

        slider_range_ms = self._slider.maximum() - self._slider.minimum() + 1
        slider_width_px = end_slider_px - start_slider_px

        # Chooses the minimum usable tick interval. Computes the spacing required for
        # the given interval, and determines if it can be fit without spacing overlaps.
        chosen_interval_sec = None
        pixels_between_ticks = None
        for tick_interval_sec in self.tick_intervals_sec:
            tick_interval_ms = tick_interval_sec * 1000
            pixels_between_ticks = slider_width_px / (slider_range_ms / tick_interval_ms)
            if pixels_between_ticks >= (self._label_width + self._label_padding):
                chosen_interval_sec = tick_interval_sec
                break

        if chosen_interval_sec is None:
            return

        # Decide the time and starting position of the first tick-mark.
        tick_x = start_slider_px + 1
        curr_time_ms = self._slider.minimum()
        if curr_time_ms % tick_interval_ms != 0:
            curr_time_ms = ((curr_time_ms + tick_interval_ms) // tick_interval_ms) * tick_interval_ms
            tick_x += slider_width_px / (slider_range_ms / (curr_time_ms - self._slider.minimum()))

        # Draw the tick marks
        self._graphics_scene.clear()
        font = self.font()
        font.setPointSize(10)
        while tick_x < end_slider_px:
            timestamp = _get_timestamp(curr_time_ms)
            self._graphics_scene.addLine(tick_x, 0, tick_x, 8)
            label = self._graphics_scene.addText(timestamp, font)
            label.setPos(tick_x - label.boundingRect().width() / 2, 9)

            tick_x += pixels_between_ticks
            curr_time_ms += tick_interval_ms

    def resizeEvent(self, e):
        """
        Overrides resizeEvent. This method resizes the tick mark bar to its new size,
        and redraws its tick marks accordingly.

        Parameters:
            e - resize event
        """
        super().resizeEvent(e)
        self._graphics_scene.setSceneRect(self.rect())
        self._reposition_tick_marks()
