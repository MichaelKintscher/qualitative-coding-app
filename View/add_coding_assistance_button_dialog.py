from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QLineEdit


class AddCodingAssistanceButtonDialog(QDialog):
    """
    A Dialog to create a new coding assistance button
    """

    def __init__(self, table):
        """
        Constructor: Initializes the layout of the Add Coding Assistance Button dialog

        Parameters:
            table - An instance of EncodingTable
        """
        super().__init__()

        self.table = table

        # Creates a vertical layout for the dialog box.
        dialog_layout = QVBoxLayout()

        apply_text_hbox = QHBoxLayout()
        apply_text_label = QLabel("Button Name: ")
        self.apply_text_field = QLineEdit()
        apply_text_hbox.addWidget(apply_text_label)
        apply_text_hbox.addWidget(self.apply_text_field)

        hotkey_hbox = QHBoxLayout()
        hotkey_label = QLabel("Assign a hotkey for this button: ")
        self.hotkey_field = QLineEdit()
        hotkey_hbox.addWidget(hotkey_label)
        hotkey_hbox.addWidget(self.hotkey_field)

        self.error_label = QLabel()

        self.create_button = QPushButton("Create Button")
        self.load_button = QPushButton("Load Button")

        dialog_layout.addLayout(apply_text_hbox)
        dialog_layout.addSpacing(50)
        dialog_layout.addLayout(hotkey_hbox)
        dialog_layout.addSpacing(50)

        self.dynamic_line_edits = []
        headers = [self.table.horizontalHeaderItem(c) for c in range(self.table.columnCount())]
        labels = [x.text() for x in headers]
        for i in range(len(labels)):
            dynamic_input_hbox = QHBoxLayout()
            dynamic_input_label = QLabel(labels[i])
            dynamic_input_field = QLineEdit()
            self.dynamic_line_edits.append(dynamic_input_field)

            dynamic_input_hbox.addWidget(dynamic_input_label)
            dynamic_input_hbox.addWidget(dynamic_input_field)
            dialog_layout.addLayout(dynamic_input_hbox)
            dialog_layout.addSpacing(50)

        dialog_layout.addWidget(self.error_label)
        dialog_layout.addWidget(self.create_button)
        dialog_layout.addWidget(self.load_button)

        self.setLayout(dialog_layout)

    def connect_create_button_to_slot(self, slot):
        """
        Connect a create_button event to a slot function in the controller.
        """
        self.create_button.clicked.connect(slot)

    def connect_load_button_to_slot(self, slot):
        """
        Connect a load_button event to a slot function in the controller.
        """
        self.load_button.clicked.connect(slot)
