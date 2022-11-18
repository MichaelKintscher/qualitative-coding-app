from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QComboBox, QStylePainter, QStyleOptionComboBox, QStyle


class PlaybackSpeedComboBox(QComboBox):
    """
    Custom Combobox widget that overrides the Paint method in order to display
    custom text on the selected combobox item.
    """
    def __init__(self):
        # Construct the QComboBox widget as usual
        super().__init__()

        # Add values from 0.25 to and including 2.0 with 0.25 increments.
        for ix in range(1, 9):
            self.addItem(str(ix / 4))
            self.setItemData(ix - 1, ix / 4)

        # Adjust the text of the 1.0 value to "Normal" and let it be the default value.
        self.setItemText(3, "Normal")
        self.setCurrentIndex(3)

    def paintEvent(self, e):
        """
        Overwritten to set the text of the combobox to include a label:
        "PLayback speed:"
        """
        # Implementation credit: Sebastien247 from Stackoverflow
        # https://stackoverflow.com/questions/16080431/qt-set-display-text-of-non-editable-qcombobox
        painter = QStylePainter(self)
        painter.setPen(self.palette().color(QPalette.Text))

        # Draw the combobox and its components.
        opt = QStyleOptionComboBox()
        self.initStyleOption(opt)
        opt.currentText = "Playback speed: " + self.currentText()
        painter.drawComplexControl(QStyle.CC_ComboBox, opt)
        painter.drawControl(QStyle.CE_ComboBoxLabel, opt)
