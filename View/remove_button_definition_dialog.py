from PySide6.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton


class RemoveButtonDefinitionDialog(QDialog):
    """
    A dialog to remove or clear button definitions
    """
    def __init__(self):
        """
        Constructor: Initializes the layout of the Remove Button Definition Dialog
        """
        super().__init__()

        dialog_layout = QVBoxLayout()

        remove_definition_hbox = QHBoxLayout()
        remove_definition_label = QLabel("Name of button definition to remove: ")
        self.remove_definition_text = QLineEdit()
        remove_definition_hbox.addWidget(remove_definition_label)
        remove_definition_hbox.addWidget(self.remove_definition_text)
        self.remove_definition_button = QPushButton("Remove Button Definition")
        self.clear_all_button = QPushButton("Clear all Button Definitions")

        dialog_layout.addLayout(remove_definition_hbox)
        dialog_layout.addWidget(self.remove_definition_button)
        dialog_layout.addSpacing(10)
        dialog_layout.addWidget(self.clear_all_button)

        self.setLayout(dialog_layout)

    def connect_remove_button_to_slot(self, slot):
        """
        Connect a remove button event to slot
        """
        self.remove_definition_button.clicked.connect(slot)

    def connect_clear_button_to_slot(self, slot):
        """
        Connect a clear all button event to slot
        """
        self.clear_all_button.clicked.connect(slot)
