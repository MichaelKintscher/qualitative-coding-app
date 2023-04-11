from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLineEdit


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
