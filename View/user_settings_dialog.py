from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QLineEdit, QComboBox


class UserSettingsDialog(QDialog):
  
    def __init__(self):
        """
        Constructor: Initializes the layout of the settings dialog
        """
        super().__init__()

        # Creates a vertical layout for the dialog box.
        dialog_layout = QVBoxLayout()

        # Creates horizontal layouts to group common widgets in the dialog.
        minimum_size_hbox = QHBoxLayout()
        maximum_width_hbox = QHBoxLayout()
        padding_hbox = QHBoxLayout()
        font_hbox = QHBoxLayout()

        # Initializes the widgets of the dialog.
        encoding_table_label = QLabel("Encoding Table Settings:")
        minimum_size_label = QLabel("Set minimum cell width and height")
        self.minimum_size_width_box = QLineEdit()
        self.minimum_size_height_box = QLineEdit()
        self.minimum_size_button = QPushButton("Change Minimum Cell Size")
        maximum_width_label = QLabel("Set maximum cell width")
        self.maximum_width_text_box = QLineEdit()
        self.maximum_width_button = QPushButton("Set Maximum Cell Width")
        padding_label = QLabel("Set cell padding")
        self.padding_text_box = QLineEdit()
        self.padding_button = QPushButton("Set Padding")
        """Creates font changing label and dropdown"""
        font_options = ["8", "9", "10", "11", "12", "14", "16",
                        "18", "20", "22", "24", "26", "28", "36", "48", "72"]
        self.change_font_label = QLabel("Change font: ")
        self.change_font_dropDown = QComboBox()
        self.change_font_dropDown.addItems(font_options)

        # Adds the widgets to the internal layouts.
        minimum_size_hbox.addWidget(self.minimum_size_width_box)
        minimum_size_hbox.addWidget(self.minimum_size_height_box)
        minimum_size_hbox.addWidget(self.minimum_size_button)
        maximum_width_hbox.addWidget(self.maximum_width_text_box)
        maximum_width_hbox.addWidget(self.maximum_width_button)
        padding_hbox.addWidget(self.padding_text_box)
        padding_hbox.addWidget(self.padding_button)
        font_hbox.addWidget(self.change_font_label)
        font_hbox.addWidget(self.change_font_dropDown)

        # Adds a title for the encoding table settings to the dialog.
        dialog_layout.addWidget(encoding_table_label)

        # Adds all the widgets to the main layout.
        dialog_layout.addSpacing(50)
        dialog_layout.addWidget(minimum_size_label)
        dialog_layout.addLayout(minimum_size_hbox)
        dialog_layout.addSpacing(50)
        dialog_layout.addWidget(maximum_width_label)
        dialog_layout.addLayout(maximum_width_hbox)
        dialog_layout.addSpacing(50)
        dialog_layout.addWidget(padding_label)
        dialog_layout.addLayout(padding_hbox)
        dialog_layout.addSpacing(50)
        dialog_layout.addLayout(font_hbox)

        # Sets the layout of the dialog.
        self.setLayout(dialog_layout)

    def connect_cell_size_to_slot(self, slot):
        """
        Connects a minimum_size_button event to a slot function in the controller.
        """
        self.minimum_size_button.clicked.connect(slot)

    def connect_maximum_size_to_slot(self, slot):
        """
        Connects a maximum_width_button event to a slot function in the controller.
        """
        self.maximum_width_button.clicked.connect(slot)

    def connect_padding_to_slot(self, slot):
        """
        Connects a padding_button event to a slot function in the controller.
        """
        self.padding_button.clicked.connect(slot)

    def connect_font_to_slot(self, slot):
        """
        Connects a change_font event to a slot function in the controller.
        """
        self.change_font_dropDown.activated.connect(slot)
