import PySide6
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

from View.button_panel import ButtonPanel


class CodingAssistancePanel(QWidget):
    """Container of all Coding Assistance related widgets."""

    def __init__(self):
        """
        Constructor - Creates the related Coding Assistance widgets and adds them
        to the panel using a QVBoxLayout.
        """
        super().__init__()

        self._title = QLabel("Coding Assistance Buttons")
        self.button_panel = ButtonPanel()

        # Center the title in the panel.
        self._title.setAlignment(PySide6.QtCore.Qt.AlignCenter)

        # Create empty widgets to pad the panel.
        empty_widget_top = QWidget()
        empty_widget_bottom = QWidget()

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(empty_widget_top, stretch=4)
        vertical_layout.addWidget(self._title, stretch=1)
        vertical_layout.addWidget(self.button_panel, stretch=2)
        vertical_layout.addWidget(empty_widget_bottom, stretch=4)
        self.setLayout(vertical_layout)
