from PySide6.QtCore import Qt, Slot, QPoint
from PySide6.QtWidgets import QWidget, QSizePolicy, QApplication, QLineEdit, QGridLayout
from superqt import QRangeSlider


class ScalingBar(QWidget):
    """
    The ScalingBar is a custom QRangeSlider, providing timestamp labels
    above each handle. The Scaling Bar is a slider which allows the user
    to scale the zoom level of the scrubber bar.
    """

    def __init__(self, timestamp_width):
        """
        Constructs an instance of the scaling bar.

        Parameters:
            timestamp_width - width of the timestamp labels to use.
        """
        super().__init__()

        self._timestamp_width = timestamp_width
        self._slider = QRangeSlider(Qt.Orientation.Horizontal)
        self._slider.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

        self._min_label = TimestampLabel(self._slider, self._slider, self._timestamp_width)
        self._max_label = TimestampLabel(self._slider, self._slider, self._timestamp_width)
        self._handle_labels = [self._min_label, self._max_label]

        # For fine-tuning label positions
        self.label_shift_x = 3
        self._label_shift_y = 0

        self._slider.valueChanged.connect(self._on_value_changed)
        self._slider.rangeChanged.connect(self._on_range_changed)

        self._on_value_changed(self._slider.value())
        self._on_range_changed(self._slider.minimum(), self._slider.maximum())

        self._set_layout()

    def get_slider(self):
        """
        Gets a reference to the slider in the Scaling Bar widget.

        Returns:
            reference to the slider in the widget.
        """
        return self._slider

    def resizeEvent(self, e):
        """
        On the event that the slider resizes, we update the handle labels
        accordingly.

        Parameters:
            e - resize event
        """
        self._slider.resizeEvent(e)
        self._reposition_labels()

    @Slot(int, int)
    def _on_range_changed(self, range_min, range_max):
        """
        Event-handler for slider range changes. Updates and repositions the
        timestamp labels according to the new range.

        Parameters:
            range_min - minimum value of the slider (milliseconds).
            range_max - maximum value of the slider (milliseconds).
        """
        if (range_min, range_max) != (self._slider.minimum(), self._slider.maximum()):
            self._slider.setRange(range_min, range_max)
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
            rect = self._slider._handleRect(i)
            dx = -label.width() / 2
            dy = -label.height() / 2
            dy *= 3.5
            pos = self._slider.mapToParent(rect.center())
            pos += QPoint(int(dx + self.label_shift_x), int(dy + self._label_shift_y))
            if last_edge is not None:
                # prevent label overlap
                pos.setX(int(max(pos.x(), last_edge.x() + label.width() / 2 + 20)))
            label.move(pos)
            last_edge = pos
            label.clearFocus()
            label.show()
        self._slider.update()
        self.update()

    def _set_layout(self):
        """
        Sets the layout of the scaling bar widget, allowing all of its
        components to live in a layout for viewing purposes.
        """
        layout = QGridLayout()
        layout.setSpacing(0)
        self._slider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(self._min_label, 0, 0)
        layout.addWidget(self._slider, 0, 0)
        layout.addWidget(self._max_label, 0, 0)

        old_layout = self.layout()
        if old_layout is not None:
            QWidget().setLayout(old_layout)

        self.setLayout(layout)
        label_size = self._timestamp_width
        margin_side = int(label_size / 2)
        layout.setContentsMargins(margin_side, 25, margin_side, 0)
        QApplication.processEvents()
        self._reposition_labels()


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


class TimestampLabel(QLineEdit):
    """
    Custom timestamp label, which presents the timestamp in a fixed
    sized QLineEdit.

    Note: A QLabel was not used as changes to its text triggered
    layout updates.
    """

    def __init__(self, slider, parent, timestamp_width):
        """
        Constructs an instance of the timestamp label.

        Parameters:
            label - slider which the label acts on.
            parent - parent of the slider.
            timestamp_width - width of a timestamp label
        """
        super().__init__(parent=parent)
        self._slider = slider

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("background: transparent; border: 0; color: black")

        self.setFixedWidth(timestamp_width)

        # Don't allow the user to edit the label.
        self.setEnabled(False)

    def set_value(self, value):
        """
        Sets the timestamp value of the label according to the given
        microsecond value.
        Parameters:
            value - millisecond duration.
        """
        timestamp = convert_ms_to_timestamp(value)
        self.setText(timestamp)
