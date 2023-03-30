from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class ButtonDefinitionListElement(QWidget):
    """
    The Button Definition List Element is a widget container for button definitions to be presented in the
    user settings page.
    """

    def __init__(self, button_definition):
        """
        Constructs an instance of the ButtonDefinitionListElement object, declaring the
        button definition and other related fields as public class members.
        """
        super().__init__()

        button_definition_layout = QVBoxLayout()

        self.element_id = button_definition.button_id

        button_definition_layout.addWidget(QLabel("Button: " + button_definition.button_id))
        for data_index, data in enumerate(button_definition.data):
            column_number = data_index + 1
            button_definition_layout.addWidget(QLabel("Column " + str(column_number) + " Data: " + data))

        self.setLayout(button_definition_layout)
