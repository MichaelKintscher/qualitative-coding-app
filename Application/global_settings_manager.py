from PySide6.QtCore import QSettings

from Models.button_definition_entity import ButtonDefinitionEntity
from Models.global_settings_entity import GlobalSettingsEntity


class GlobalSettingsManager:
    """
    GlobalSettingsManager is a manager for the settings that can be applied to
    all sessions.
    """
    def __init__(self):
        """
        Constructor - Creates an instance of GlobalSettingsManager
        """
        self.global_settings_entity = GlobalSettingsEntity()

    def add_button_definition(self, button_definition):
        """
        Add a button definition to the button definition list
        """
        self.global_settings_entity.button_definitions.append(button_definition)
        self.save_encoding_button_definitions()

    def remove_button_definition(self, button_definition):
        """
        Remove a button definition from the button definition list
        """
        self.global_settings_entity.button_definitions.remove(button_definition)
        self.save_encoding_button_definitions()

    def get_button_definition(self, button_id):
        """
        Return a button definition from the button definition list
        """
        for button_definition in self.global_settings_entity.button_definitions:
            if button_id == button_definition.button_id:
                return button_definition
        return None

    def save_encoding_button_definitions(self):
        """
        Update the global settings
        """
        settings = QSettings()

        settings.beginGroup("global-settings")
        settings.beginGroup("encoding-buttons")

        settings.beginWriteArray("button-definitions", len(self.global_settings_entity.button_definitions))
        for index, button_definition in enumerate(self.global_settings_entity.button_definitions):
            settings.setArrayIndex(index)
            settings.setValue("button-id", button_definition.button_id)
            settings.beginWriteArray("data", len(button_definition.data))
            for data_index, data_item in enumerate(button_definition.data):
                settings.setArrayIndex(data_index)
                settings.setValue("data-item", data_item)
            settings.endArray()
        settings.endArray()

        settings.endGroup()  # encoding-buttons
        settings.endGroup()  # global-settings

    def load_global_settings(self):
        """
        Load the global settings
        """
        settings = QSettings()

        settings.beginGroup("global-settings")

        settings.beginGroup("user-settings")

        # Sets the padding and the max width to global settings entity
        self.global_settings_entity.table_padding = int(settings.value("table_padding"))
        self.global_settings_entity.table_maximum_width = int(settings.value("table_maximum_width"))

        # Sets the cell size with width, index 0, and height, index 1 to global settings entity
        self.global_settings_entity.table_cell_size.append(int(settings.value("table_cell_size_width")))
        self.global_settings_entity.table_cell_size.append(int(settings.value("table_cell_size_height")))

        # Sets the font size to global settings entity.
        print(settings.value(("table_font_size")))
        # self.global_settings_entity.table_font_size = int(settings.value("table_font_size"))

        settings.endGroup()  # user-settings

        settings.beginGroup("encoding-buttons")

        button_definitions_length = settings.beginReadArray("button-definitions")
        for index in range(button_definitions_length):
            settings.setArrayIndex(index)
            button_id = settings.value("button-id")
            data = []
            data_length = settings.beginReadArray("data")
            for data_index in range(data_length):
                settings.setArrayIndex(data_index)
                data.append(settings.value("data-item"))
            settings.endArray()
            button_definition = ButtonDefinitionEntity(button_id, data)
            self.global_settings_entity.button_definitions.append(button_definition)
        settings.endArray()

        settings.endGroup()  # encoding-buttons
        settings.endGroup()  # global-settings

    def save_user_settings(self):
        """
        Saves the values in the global settings entity to Qsettings
        """
        settings = QSettings()

        settings.beginGroup("global-settings")

        settings.beginGroup("user-settings")

        # Sets the padding and the max width.
        settings.setValue("table_padding", self.global_settings_entity.table_padding)
        settings.setValue("table_maximum_width", self.global_settings_entity.table_maximum_width)

        # Sets the cell size with width, index 0, and height, index 1.
        settings.setValue("table_cell_size_width", self.global_settings_entity.table_cell_size[0])
        settings.setValue("table_cell_size_height", self.global_settings_entity.table_cell_size[1])

        # Sets the table font size.
        settings.setValue("table_font_size", self.global_settings_entity.table_font_size)

        settings.endGroup()
        settings.endGroup()

    def set_table_padding(self, table_padding):
        """
        Setter method to set the cell padding to the global settings entity.

        Parameter:
            Int representing the padding in each table cell.
        """
        self.global_settings_entity.table_padding = table_padding

    def set_table_cell_size(self, table_cell_size):
        """
        Setter method to set the cell size to the global settings entity.

        Parameter:
            List of ints with index 0 holding the width and index 1 holding the height.
        """
        self.global_settings_entity.table_cell_size = table_cell_size

    def set_table_maximum_width(self, table_maximum_width):
        """
        Setter method to set the cell max width to the global settings entity.

        Parameter:
            Int representing the max width of each table cell.
        """
        self.global_settings_entity.table_maximum_width = table_maximum_width

    def set_table_font_size(self, table_font_size):
        """
        Setter method to set the table font size to the global settings entity.

        Parameter:
            Int representing the table font size.
        """
        self.global_settings_entity.table_font_size = table_font_size

