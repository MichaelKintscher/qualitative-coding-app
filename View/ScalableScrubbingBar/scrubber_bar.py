from PySide6.QtCore import Qt, QRect, Signal, Slot
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import QSlider, QStyleOptionSlider, QStyle


class ScrubberBar(QSlider):
    """
    Implementation of a scrubber bar where the range is dynamically altered
    based on the values of the scaling bar, and the handle is hidden when
    our privately tracked _value state is out of bounds. This variable is
    important since the parent's value is bounded strictly by the slider's
    range, whereas our variable is not.
    """
    onValueChanged = Signal(int)

    def __init__(self, scaling_bar):
        """
        Constructs an instance of the scrubber bar. The passed in scaling bar is
        the slider whose value dictates the range of this slider.

        Parameters:
            scaling_bar - slider which scales this.
        """
        super().__init__(Qt.Orientation.Horizontal)
        self._value = 0
        scaling_bar.valueChanged.connect(lambda val: self.setRange(val[0], val[1]))
        self.sliderMoved.connect(self._slider_moved)

    def setRange(self, minimum, maximum):
        """
        Override. Upon updating the range of the slider, if the current value
        is greater than or equal to the new range, then the value is set to the
        minimum or maximum. This override method sets the value of the slider to
        our privately tracked value variable.

        Parameters:
            minimum - minimum value this slider represents
            maximum - maximum value this slider represents
        """
        super().setRange(minimum, maximum)
        super().setValue(self._value)

    def setValue(self, value):
        """
        Override. The value is only set to the slider if it's within the
        valid range, otherwise we don't set it. However, we do keep track
        of the value in our privately stored value variable.

        Parameters:
            value - value of the slider to set
        """
        if self.minimum() <= value <= self.maximum():
            super().setValue(value)
        self._value = value
        self.onValueChanged.emit(self._value)
        self.update()

    def paintEvent(self, e):
        """
        Complete override of slider painting. This method will hide the handle if our
        privately stored value variable is outside the bounds of the current range.

        Parameters:
            e - paint event
        """
        painter = QPainter(self)
        opt = QStyleOptionSlider()
        self.initStyleOption(opt)

        # Draw the default groove (bar)
        opt.subControls = QStyle.SC_SliderGroove

        # Get the style information of the groove and handle.
        groove_rect = self.style().subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderGroove, self)
        handle_rect = self.style().subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderHandle, self)

        # Create a rectangle to fill the progress from the start of the slider to the handle.
        #   This is overriden because the default progress rect will not occupy the entire
        #   bar when the handle is hidden.
        progress_rect = QRect(groove_rect.left(),
                              groove_rect.top() + 1,
                              handle_rect.left() + 1,
                              groove_rect.height() - 2)
        if self._value > self.maximum():
            progress_rect.setWidth(groove_rect.width())

        # Draw the handle if the privately stored value variable is in view.
        if self.minimum() <= self._value <= self.maximum():
            opt.subControls |= QStyle.SC_SliderHandle
            self.setEnabled(True)   # Make it interactive
        else:
            self.setEnabled(False)  # Even though it's not painted, it's still there. Make it immovable.

        self.style().drawComplexControl(QStyle.CC_Slider, opt, painter, self)

        # Finally, if there is progress to be shown, draw the progress rect.
        if self._value >= self.minimum():
            painter.setBrush(QColor(68, 160, 217))
            painter.setPen(QColor(40, 99, 132))
            painter.drawRect(progress_rect)

    @Slot(tuple)
    def _slider_moved(self, value):
        """
        Upon the user sliding the handle, we update our privately stored value variable
        to the most up-to-date value.
        """
        self._value = value
        self.onValueChanged.emit(self._value)
