from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QLineEdit, QScrollArea, QWidget

from View.button_definition_list_element import ButtonDefinitionListElement


class UserSettingsDialog(QDialog):
  
    def __init__(self, button_definitions):
        """
        Constructor: Initializes the layout of the settings dialog
        """
        super().__init__()

        # Creates a vertical layout for the dialog box.
        dialog_layout = QVBoxLayout()
        self.element_list = []

        # Creates a basic title for the button definition settings
        button_definition_label = QLabel("Button Definition Settings")
        dialog_layout.addWidget(button_definition_label)

        # Initializes button definition settings widgets and inserts them in the dialog
        self.edit_button = QPushButton("Edit Definition")
        self.remove_button = QPushButton("Remove Definition")
        self.button_definition_list = self.create_button_definition_list(button_definitions)

        # Creates a scroll area widget and adds the button definition widget to it
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.button_definition_list)

        # Adds the scroll area widget to the main layout of the dialog
        dialog_layout.addWidget(scroll_area)

        # Adds the edit and remove buttons to the main layout of the dialog
        edit_remove_button_hbox = QHBoxLayout()
        edit_remove_button_hbox.addWidget(self.edit_button)
        edit_remove_button_hbox.addWidget(self.remove_button)
        dialog_layout.addLayout(edit_remove_button_hbox)

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

        self.setLayout(dialog_layout)

    @staticmethod
    def create_button_definition_list(button_definitions):
        """
        Creates a widget containing a vertical layout of the list of button definitions
        """
        container_widget = QWidget()
        button_definition_layout = QVBoxLayout()

        for button_definition in button_definitions:
            button_definition_list_element = ButtonDefinitionListElement(button_definition)
            button_definition_layout.addWidget(button_definition_list_element)
            button_definition_layout.addSpacing(10)
        button_definition_layout.addSpacing(20)

        container_widget.setLayout(button_definition_layout)
        return container_widget

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
    
