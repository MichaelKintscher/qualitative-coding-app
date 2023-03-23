from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QLineEdit, QScrollArea, QWidget


class UserSettingsDialog(QDialog):
  
    def __init__(self, button_definitions):
        """
        Constructor: Initializes the layout of the settings dialog
        """
        super().__init__()

        # Creates a vertical layout for the dialog box.
        dialog_layout = QVBoxLayout()

        # Initializes button definition settings widgets and inserts them in the dialog
        dialog_layout.addWidget(QLabel("Encoding Button Definitions"))
        dialog_layout.addSpacing(5)
        for button_definition in button_definitions:
            dialog_layout.addWidget(QLabel("Button: " + button_definition.button_id))
            for data_index, data in enumerate(button_definition.data):
                column_number = data_index + 1
                dialog_layout.addWidget(QLabel("Column " + str(column_number) + " Data: " + data))
            dialog_layout.addSpacing(10)
        edit_remove_button_hbox = QHBoxLayout()
        self.edit_button = QPushButton("Edit Definition")
        self.remove_button = QPushButton("Remove Definition")
        edit_remove_button_hbox.addWidget(self.edit_button)
        edit_remove_button_hbox.addWidget(self.remove_button)
        dialog_layout.addLayout(edit_remove_button_hbox)
        dialog_layout.addSpacing(20)

        # Creates horizontal layouts to group common encoding table settings widgets in the dialog.
        minimum_size_hbox = QHBoxLayout()
        maximum_width_hbox = QHBoxLayout()
        padding_hbox = QHBoxLayout()

        # Initializes encoding table settings widgets
        encoding_table_label = QLabel("Encoding Table Settings")
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

        # Adds the widgets to the internal layouts.
        minimum_size_hbox.addWidget(self.minimum_size_width_box)
        minimum_size_hbox.addWidget(self.minimum_size_height_box)
        minimum_size_hbox.addWidget(self.minimum_size_button)
        maximum_width_hbox.addWidget(self.maximum_width_text_box)
        maximum_width_hbox.addWidget(self.maximum_width_button)
        padding_hbox.addWidget(self.padding_text_box)
        padding_hbox.addWidget(self.padding_button)

        # Adds a title for the encoding table settings to the dialog.
        dialog_layout.addWidget(encoding_table_label)
        dialog_layout.addSpacing(5)

        # Adds all the widgets to the main layout.
        dialog_layout.addWidget(minimum_size_label)
        dialog_layout.addLayout(minimum_size_hbox)
        dialog_layout.addSpacing(10)
        dialog_layout.addWidget(maximum_width_label)
        dialog_layout.addLayout(maximum_width_hbox)
        dialog_layout.addSpacing(10)
        dialog_layout.addWidget(padding_label)
        dialog_layout.addLayout(padding_hbox)

        # Sets the layout of the dialog using a QScrollArea.
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area_widget = QWidget()
        scroll_area.setWidget(scroll_area_widget)
        scroll_area_layout = QVBoxLayout(scroll_area_widget)
        scroll_area_layout.addLayout(dialog_layout)
        self.setLayout(QVBoxLayout(self))
        self.layout().addWidget(scroll_area)
        scroll_area_widget.adjustSize()
        scroll_area_widget.setMinimumHeight(scroll_area_widget.sizeHint().height())

    def connect_edit_button_to_slot(self, slot):
        """
        Connects an edit button event to a slot function in the controller.
        """
        self.edit_button.clicked.connect(slot)

    def connect_remove_button_to_slot(self, slot):
        """
        Connects a remove button event to a slot function in the controller.
        """
        self.remove_button.clicked.connect(slot)

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
    
