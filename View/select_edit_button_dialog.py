from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton


class SelectEditButtonDialog(QDialog):
    """
    A Dialog to select a button definition to be edited
    """
    def __init__(self):
        """
        Constructor: Initializes the layout of the Select Edit Button dialog
        """
        super().__init__()

        dialog_layout = QVBoxLayout()

        button_name_hbox = QHBoxLayout()
        button_name_label = QLabel("Name of button to edit: ")
        self.button_name_textbox = QLineEdit()
        button_name_hbox.addWidget(button_name_label)
        button_name_hbox.addWidget(self.button_name_textbox)

        self.edit_button = QPushButton("Edit")

        dialog_layout.addLayout(button_name_hbox)
        dialog_layout.addSpacing(50)
        dialog_layout.addWidget(self.edit_button)

        self.setLayout(dialog_layout)

    def connect_edit_button_to_slot(self, slot):
        """
        Connect a edit_button event to a slot function in the controller.
        """
        self.edit_button.clicked.connect(slot)