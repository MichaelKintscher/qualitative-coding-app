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
        self.update_saved_settings()

    def remove_button_definition(self, button_definition):
        """
        Remove a button definition from the button definition list
        """
        self.global_settings_entity.button_definitions.remove(button_definition)
        self.update_saved_settings()

    def get_button_hotkeys(self):
        """
        Return the list of button hotkeys from the button definition list
        """
        return [button_definition.hotkey for button_definition in self.global_settings_entity.button_definitions]

    def get_button_definition(self, button_id):
        """
        Return a button definition from the button definition list
        """
        for button_definition in self.global_settings_entity.button_definitions:
            if button_id == button_definition.button_id:
                return button_definition
        return None

    def update_saved_settings(self):
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
            settings.setValue("hotkey", button_definition.hotkey)
            settings.beginWriteArray("data", len(button_definition.data))
            for data_index, data_item in enumerate(button_definition.data):
                settings.setArrayIndex(data_index)
                settings.setValue("data-item", data_item)
            settings.endArray()
        settings.endArray()

        settings.endGroup() # global-settings
        settings.endGroup() # encoding-buttons

    def load_global_settings(self):
        """
        Load the global settings
        """
        settings = QSettings()

        settings.beginGroup("global-settings")
        settings.beginGroup("encoding-buttons")

        button_definitions_length = settings.beginReadArray("button-definitions")
        for index in range(button_definitions_length):
            settings.setArrayIndex(index)
            button_id = settings.value("button-id")
            hotkey = settings.value("hotkey")
            data = []
            data_length = settings.beginReadArray("data")
            for data_index in range(data_length):
                settings.setArrayIndex(data_index)
                data.append(settings.value("data-item"))
            settings.endArray()
            button_definition = ButtonDefinitionEntity(button_id, hotkey, data)
            self.global_settings_entity.button_definitions.append(button_definition)
        settings.endArray()

        settings.endGroup()
        settings.endGroup()