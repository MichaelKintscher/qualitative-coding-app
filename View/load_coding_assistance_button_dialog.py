from PySide6.QtWidgets import QDialog, QCheckBox, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QLineEdit, QRadioButton


class LoadCodingAssistanceButtonDialog(QDialog):

    def __init__(self, button_definitions):
        """
        Constructor: Initializes the layout of the Add Coding Assistance Button dialog
        """
        super().__init__()

        dialog_layout = QVBoxLayout()
        self.radio_buttons = []

        for button_definition in button_definitions:
            radio_button = QRadioButton("Button Name: " + button_definition.button_id)
            self.radio_buttons.append(radio_button)
            dialog_layout.addWidget(radio_button)

        self.load_button = QPushButton("Load Button")

        hotkey_hbox = QHBoxLayout()
        hotkey_label = QLabel("Assign a hotkey to this button")
        self.hotkey_textfield = QLineEdit()
        hotkey_hbox.addWidget(hotkey_label)
        hotkey_hbox.addWidget(self.hotkey_textfield)

        self.error_label = QLabel()

        dialog_layout.addLayout(hotkey_hbox)
        dialog_layout.addWidget(self.error_label)
        dialog_layout.addWidget(self.load_button)
        self.setLayout(dialog_layout)

    def connect_load_button_to_slot(self, slot, dialog):
        """
        Connect a load_button event to a slot function in the controller.
        """
        self.load_button.clicked.connect(slot)
        self.load_button.clicked.connect(dialog.close)