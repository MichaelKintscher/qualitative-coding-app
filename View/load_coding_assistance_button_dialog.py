from PySide6.QtWidgets import QDialog, QCheckBox, QVBoxLayout, QPushButton

from Models.button_definition_entity import ButtonDefinitionEntity


class LoadCodingAssistanceButtonDialog(QDialog):

    def __init__(self, button_definitions):
        """
        Constructor: Initializes the layout of the Add Coding Assistance Button dialog
        """
        super().__init__()

        dialog_layout = QVBoxLayout()
        self.checkboxes = []

        for button_definition in button_definitions:
            checkbox = QCheckBox("Button Name: " +
                                 button_definition.button_id +
                                 " Button Hotkey: " +
                                 button_definition.hotkey)
            self.checkboxes.append(checkbox)
            dialog_layout.addWidget(checkbox)

        self.load_button = QPushButton("Load Buttons Selected")

        dialog_layout.addWidget(self.load_button)
        self.setLayout(dialog_layout)

    def connect_load_button_to_slot(self, slot):
        """
        Connect a load_button event to a slot function in the controller.
        """
        self.load_button.clicked.connect(slot)