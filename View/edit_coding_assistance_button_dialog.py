from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton

from Models.button_definition_entity import ButtonDefinitionEntity


class EditCodingAssistanceButtonDialog(QDialog):
    """
    A Dialog to edit a button definition
    """
    def __init__(self, table):
        """
        Constructor: Initializes the layout of the Edit Coding Assistance Button Dialog
        """
        super().__init__()

        dialog_layout = QVBoxLayout()

        self.table = table

        button_id_hbox = QHBoxLayout()
        button_id_label = QLabel("Name: ")
        self.button_id_textbox = QLineEdit()
        button_id_hbox.addWidget(button_id_label)
        button_id_hbox.addWidget(self.button_id_textbox)

        dialog_layout.addLayout(button_id_hbox)
        dialog_layout.addSpacing(50)

        self.dynamic_line_edits = []
        headers = [self.table.horizontalHeaderItem(c) for c in range(self.table.columnCount())]
        labels = [x.text() for x in headers if x]
        i = 1
        while i in range(len(labels)):
            dynamic_input_hbox = QHBoxLayout()
            dynamic_input_label = QLabel(labels[i])
            dynamic_input_field = QLineEdit()
            self.dynamic_line_edits.append(dynamic_input_field)

            dynamic_input_hbox.addWidget(dynamic_input_label)
            dynamic_input_hbox.addWidget(dynamic_input_field)
            dialog_layout.addLayout(dynamic_input_hbox)
            dialog_layout.addSpacing(50)

            i += 1

        self.edit_button = QPushButton("Edit")
        dialog_layout.addWidget(self.edit_button)

        self.error_label = QLabel()
        dialog_layout.addWidget(self.error_label)

        self.setLayout(dialog_layout)

    def connect_edit_button_to_slot(self, slot, dialog):
        """
        Connect an edit_button event to a slot function in the controller.
        """
        self.edit_button.clicked.connect(slot)
        self.edit_button.clicked.connect(dialog.close)
