from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton


class DeleteCodingAssistanceButtonDialog(QDialog):

    def __init__(self):
        """
        Constructor: Initializes the layout of the Delete Coding Assistance Button dialog
        """
        super().__init__()

        dialog_layout = QVBoxLayout()

        button_name_hbox = QHBoxLayout()
        button_name_label = QLabel("Name of button to delete: ")
        self.button_name_textbox = QLineEdit()
        button_name_hbox.addWidget(button_name_label)
        button_name_hbox.addWidget(self.button_name_textbox)

        self.delete_button = QPushButton("Delete")

        dialog_layout.addLayout(button_name_hbox)
        dialog_layout.addSpacing(50)
        dialog_layout.addWidget(self.delete_button)

        self.setLayout(dialog_layout)

    def connect_delete_button_to_slot(self, slot, dialog):
        """
        Connect a delete_button event to a slot function in the controller.
        """
        self.delete_button.clicked.connect(slot)
        self.delete_button.clicked.connect(dialog.close)
