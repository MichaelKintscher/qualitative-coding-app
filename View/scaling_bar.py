from PySide6.QtCore import Qt, Slot, QPoint, QSize
from PySide6.QtGui import QFontMetrics
from PySide6.QtWidgets import QLabel
from superqt import QRangeSlider


class ScalingBar(QRangeSlider):
    """
    The ScalingBar is a custom QRangeSlider, providing timestamp labels
    above each handle. The Scaling Bar is a slider which allows the user
    to scale the zoom level of the scrubber bar.
    """

    def __init__(self):
        """
        Constructs an instance of the scaling bar.
        """
        super().__init__(Qt.Orientation.Horizontal)

        self._min_label = TimestampLabel(self, self)
        self._max_label = TimestampLabel(self, self)
        self._handle_labels = [self._min_label, self._max_label]

        # For fine-tuning label positions
        self.label_shift_x = -5.5
        self._label_shift_y = -1

        self.valueChanged.connect(self._on_value_changed)
        self.rangeChanged.connect(self._on_range_changed)

        self._on_value_changed(self.value())
        self._on_range_changed(self.minimum(), self.maximum())

    def resizeEvent(self, e):
        """
        On the event that the slider resizes, we update the handle labels
        accordingly.

        Parameters:
            e - resize event
        """
        super().resizeEvent(e)
        self._reposition_labels()

    def sizeHint(self):
        size = super().sizeHint()
        return QSize(size.width(), size.height() + 25)

    @Slot(int, int)
    def _on_range_changed(self, range_min, range_max):
        """
        Event-handler for slider range changes. Updates and repositions the
        timestamp labels according to the new range.

        Parameters:
            range_min - minimum value of the slider (milliseconds).
            range_max - maximum value of the slider (milliseconds).
        """
        if (range_min, range_max) != (self.minimum(), self.maximum()):
            self.setRange(range_min, range_max)
        self._reposition_labels()

    @Slot(tuple)
    def _on_value_changed(self, value):
        """
        Event-handler for slider value changes. Updates and repositions the
        timestamp labels according to the new value.

        Parameters:
            value - tuple containing the min and max handle values (milliseconds).
        """
        min_val, max_val = value
        self._min_label.set_value(min_val)
        self._max_label.set_value(max_val)
        self._reposition_labels()

    def _reposition_labels(self):
        """
        Repositions the labels on the slider according to their values.
        """
        last_edge = None
        for i, label in enumerate(self._handle_labels):
            rect = self._handleRect(i)
            dx = -label.width() / 2
            dy = -label.height() / 2
            dy *= 3.5
            pos = self.mapToParent(rect.center())
            pos += QPoint(int(dx + self.label_shift_x), int(dy + self._label_shift_y))
            if last_edge is not None:
                # prevent label overlap
                pos.setX(int(max(pos.x(), last_edge.x() + label.width() / 2 + 20)))
            if i == 0 and (rect.center().x() + dx / 2) < self.contentsRect().left():
                pos.setX(int(pos.x() - dx / 2))
            if i == 1 and (rect.center().x() - dx / 2) > self.contentsRect().right() - 10:
                pos.setX(int(pos.x() + dx / 2))
            label.move(pos)
            last_edge = pos
            label.show()
        self.update()


def convert_ms_to_timestamp(milliseconds):
    """
    Converts the given millisecond value to a timestamp.

    Parameters:
        milliseconds - milliseconds to convert.
    """
    seconds = (milliseconds // 1000) % 60
    minutes = (milliseconds // (1000 * 60)) % 60
    hours = milliseconds // (1000 * 60 * 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


class TimestampLabel(QLabel):
    """
    Custom timestamp label, which presents the timestamp in a dynamically
    sized QLabel.
    """

    def __init__(self, slider, parent):
        """
        Constructs an instance of the timestamp label.

        Parameters:
            label - slider which the label acts on.
            parent - parent of the slider.
        """
        super().__init__(parent=parent)
        self._slider = slider

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("background: transparent; border: 0")

        self._slider.rangeChanged.connect(self._update_size)
        self._update_size()

    def set_value(self, value):
        """
        Sets the timestamp value of the label according to the given
        microsecond value.

        Parameters:
            value - millisecond duration.
        """
        timestamp = convert_ms_to_timestamp(value)
        self.setText(timestamp)
        self._update_size()

    def _update_size(self):
        """
        Updates the size of the label according to its text content.
        """
        text = self.text()
        font_metrics = QFontMetrics(self.font())

        padding = 25
        self.setFixedWidth(font_metrics.horizontalAdvance(text) + padding)
