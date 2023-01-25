from PySide6.QtCore import QObject
from PySide6.QtGui import QKeySequence
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QSizePolicy, QGridLayout


class ButtonPanel(QWidget):
    """Container of all Coding Assistance buttons."""

    def __init__(self):
        """
        Constructor - Creates the Coding Assistance buttons and adds them
        into a QVBoxLayout.
        """
        super().__init__()

        button_container = QWidget()
        self.vertical_layout = QVBoxLayout()

        self.add_button = QPushButton("+")

        self.vertical_layout.addWidget(self.add_button)
        self.add_button.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Expanding)

        button_container.setLayout(self.vertical_layout)

        # Add css styling to the container to give it a background color.
        button_container.setProperty("class", "button-container")
        self.setStyleSheet('''
            .button-container {
                background-color: #c5cbd4;
                border: 1px solid black;
                border-radius: 5%;
            }
        ''')

        # Add the button container to the button panel.
        self.setLayout(QGridLayout())
        self.layout().addWidget(button_container)

    def connect_add_button_to_slot(self, slot):
        """
        Connects an add_button event to a slot function in the controller.
        """
        self.add_button.clicked.connect(slot)

    def create_coding_assistance_button(self, button_title, button_hotkey):
        """Adds a new_button to the Coding Assistance Panel"""
        self.new_button = QPushButton(button_title)
        self.new_button.setShortcut(button_hotkey)

        self.vertical_layout.insertWidget(0, self.new_button)
