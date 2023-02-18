from PySide6.QtCore import QObject
from PySide6.QtGui import QKeySequence
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QSizePolicy, QGridLayout, QHBoxLayout


class ButtonPanel(QWidget):
    """Container of all Coding Assistance buttons."""

    def __init__(self):
        """
        Constructor - Creates the Coding Assistance buttons and adds them
        into a QVBoxLayout.
        """
        super().__init__()

        button_container = QWidget()
        add_delete_container = QWidget()
        self.button_layout = QGridLayout()
        self.add_delete_layout = QHBoxLayout()

        self.add_button = QPushButton("+")
        self.delete_button = QPushButton("-")

        self.add_button.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Expanding)

        self.delete_button.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Expanding)

        self.add_delete_layout.addWidget(self.add_button)
        self.add_delete_layout.addWidget(self.delete_button)

        button_container.setLayout(self.button_layout)
        add_delete_container.setLayout(self.add_delete_layout)

        # Add css styling to the container to give it a background color.
        button_container.setProperty("class", "button-container")
        self.setStyleSheet('''
            .button-container {
                background-color: #c5cbd4;
                border: 1px solid black;
                border-radius: 5%;
            }
        ''')

        add_delete_container.setProperty("class", "add_delete_container")
        self.setStyleSheet('''
             .add_delete_container {
                 background-color: #c5cbd4;
                 border: 1px solid black;
                 border-radius: 5%;
            }
        ''')

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(button_container)
        self.layout().addWidget(add_delete_container)

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

    def create_coding_assistance_button(self, button_definition):
        """Adds a new_button to the Coding Assistance Panel"""
        self.button_layout.addWidget(button_definition.button)


    def delete_coding_assistance_button(self, button_name):
        """Deletes a button in the Coding Assistance Panel"""
        for i in range(self.button_layout.count()):
            button = self.button_layout.itemAt(i).widget()
            if button.objectName() == button_name:
                button.setParent(None)
