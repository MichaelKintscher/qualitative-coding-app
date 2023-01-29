from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QLineEdit


class CodingAssistanceButtonDialog(QDialog):

    def __init__(self):
        """
        Constructor: Initializes the layout of the Coding Assistance Button dialog
        """
        super().__init__()

        self.hotkeys = []

        # Creates a vertical layout for the dialog box.
        dialog_layout = QVBoxLayout()

        apply_text_hbox = QHBoxLayout()
        apply_text_label = QLabel("Button Label: ")
        self.apply_text_field = QLineEdit()
        apply_text_hbox.addWidget(apply_text_label)
        apply_text_hbox.addWidget(self.apply_text_field)

        hotkey_hbox = QHBoxLayout()
        hotkey_label = QLabel("Assign a hotkey for this button: ")
        self.hotkey_field = QLineEdit()
        hotkey_hbox.addWidget(hotkey_label)
        hotkey_hbox.addWidget(self.hotkey_field)

        self.error_label = QLabel()

        self.create_button = QPushButton("Create")

        dialog_layout.addLayout(apply_text_hbox)
        dialog_layout.addSpacing(50)
        dialog_layout.addLayout(hotkey_hbox)
        dialog_layout.addSpacing(50)
        dialog_layout.addWidget(self.error_label)
        dialog_layout.addWidget(self.create_button)

        self.setLayout(dialog_layout)

    def connect_create_button_to_slot(self, slot):
        """
        Connect a create_button event to a slot function in the controller.
        """
        self.create_button.clicked.connect(slot)
