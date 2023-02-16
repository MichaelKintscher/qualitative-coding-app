import PySide6
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGridLayout

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

        # Create a container widget that will encompass the panel widgets.
        panel_container = QWidget()

        # Create a vertical layout manager for the panel.
        vertical_layout = QVBoxLayout()
        vertical_layout.setContentsMargins(0, 10, 0, 0)

        # Add the coding assistance related widgets to a vertical layout.
        vertical_layout.addWidget(self._title)
        vertical_layout.addWidget(self.button_panel)
        panel_container.setLayout(vertical_layout)

        # Add css styling to give a border to the panel.
        panel_container.setProperty("class", "coding-panel")
        self.setStyleSheet('''
            .coding-panel {
                border: 1px solid black;
            }
        ''')

        # Add the container widget to the coding assistance panel.
        self.setLayout(QGridLayout())
        self.layout().addWidget(panel_container)
