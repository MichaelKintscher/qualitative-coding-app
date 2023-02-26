from PySide6.QtCore import QObject
from PySide6.QtGui import QKeySequence
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QSizePolicy, QGridLayout, QHBoxLayout

from View.grid_layout import GridLayout


class ButtonPanel(QWidget):
    """Container of all Coding Assistance buttons."""

    def __init__(self):
        """
        Constructor - Creates the Coding Assistance buttons and adds them
        into a QVBoxLayout.
        """
        super().__init__()

        button_container = QWidget()

        self.button_layout = QGridLayout()
        self.add_delete_layout = QHBoxLayout()

        self.horizontal_layout = QHBoxLayout()
        self.add_button = QPushButton("+")
        self.delete_button = QPushButton("-")
        add_delete_container = QWidget()

        self.add_button.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Expanding)

        self.delete_button.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Expanding)

        self.add_delete_layout.addWidget(self.add_button)
        self.add_delete_layout.addWidget(self.delete_button)

        add_delete_container.setLayout(self.add_delete_layout)

        # Add css styling to the container to give it a background color.
        button_container.setProperty("class", "button-container")
        add_delete_container.setProperty("class", "add_delete_container")
        self.setStyleSheet('''
            .button-container {
                background-color: #c5cbd4;
                border: 1px solid black;
                border-radius: 5%;
            }
        ''')

        # Layout for the button container widget.
        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.setContentsMargins(0, 0, 0, 0)

        # Create a 3x3 grid for the encoding buttons.
        grid_container = QWidget()
        self.grid_layout = GridLayout(self.parent(), 3, 3)
        grid_container.setLayout(self.grid_layout)
        grid_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.add_button = QPushButton("+")
        self.add_button.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Expanding)

        self.horizontal_layout.addWidget(self.add_button)
        self.horizontal_layout.addWidget(self.delete_button)
        button_container.setLayout(self.horizontal_layout)

        self.vertical_layout.addWidget(grid_container, stretch=10)
        self.vertical_layout.addWidget(button_container, stretch=1)

        # Add the button container to the button panel.
        self.setLayout(self.vertical_layout)

    def connect_add_button_to_slot(self, slot):
        """
        Connects an add_button event to a slot function in the controller.
        """
        self.add_button.clicked.connect(slot)

    def connect_delete_button_to_slot(self, slot):
        """
        Connects a delete_button event to a slot function in the controller.
        """
        self.delete_button.clicked.connect(slot)

    def create_coding_assistance_button(self, button):
        """
        Adds a new_button to the Coding Assistance Panel

        Parameters:
            button_definition - definition of button to create.
        """
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.grid_layout.addWidget(button)

    """def delete_coding_assistance_button(self, button_definition):
        
        Deletes a button in the Coding Assistance Panel

        Parameters:
            button_definition - definition of button to delete
        
        for i in range(self.button_layout.count()):
            button = self.grid_layout.itemAt(i).widget()
            if button.text() == button_definition.button_id:
                self.grid_layout.removeItem(button)
                return"""
