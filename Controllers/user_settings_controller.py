from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMessageBox

from Models.button_definition_entity import ButtonDefinitionEntity
from View.edit_coding_assistance_button_dialog import EditCodingAssistanceButtonDialog
from View.remove_button_definition_dialog import RemoveButtonDefinitionDialog
from View.select_edit_button_dialog import SelectEditButtonDialog
from View.user_settings_dialog import UserSettingsDialog


class UserSettingsController:
    """
    The WindowController responds to input events from the Window. The Controller
    handles the main logic of the application.
    """
    def __init__(self, global_settings_manager):
        self.global_settings_manager = global_settings_manager
        self.user_settings = None
        self._window_controller = None

    def get_dialog(self):
        """
        Gets a reference to the user settings dialog.

        Returns:
            reference to the user settings dialog.
        """
        return self.user_settings

    @Slot()
    def edit_coding_assistance_button(self):
        """
        Edit a button definition in Global Settings
        """
        edit_button_id = self.select_edit_button_dialog.button_name_textbox.text()
        for button_definition in self.global_settings_manager.global_settings_entity.button_definitions:
            if edit_button_id == button_definition.button_id:
                button_id = self.edit_button_dialog.button_id_textbox.text()
                data = []
                for line_edit in self.edit_button_dialog.dynamic_line_edits:
                    data.append(line_edit.text())
                new_button_definition = ButtonDefinitionEntity(button_id, data)
                self.global_settings_manager.remove_button_definition(button_definition)
                self.global_settings_manager.add_button_definition(new_button_definition)

    @Slot()
    def open_edit_coding_assistance_button_dialog(self):
        """
        Open a dialog to edit a Coding Assistance Button
        """
        self.edit_button_dialog = EditCodingAssistanceButtonDialog(self._window_controller._window.table_panel.table)
        self.edit_button_dialog.connect_edit_button_to_slot(self.edit_coding_assistance_button)
        self.edit_button_dialog.exec()

    @Slot()
    def open_select_edit_button_dialog(self):
        """
        Open a dialog to select a Coding Assistance Button to edit
        """
        self.select_edit_button_dialog = SelectEditButtonDialog()
        self.select_edit_button_dialog.connect_edit_button_to_slot(
            self.open_edit_coding_assistance_button_dialog)
        self.select_edit_button_dialog.exec()

    @Slot()
    def remove_button_definition(self):
        """
        Remove a button definition from Global Settings and the
        button definition list inside the User Settings Dialog
        """
        button_id = self.remove_button_definition_dialog.remove_definition_text.text()
        button_definition_list = self.user_settings.button_definition_list.layout()

        for i in range(button_definition_list.count()):
            element = button_definition_list.itemAt(i)
            if element and element.widget():
                if element.widget().element_id == button_id:
                    element.widget().deleteLater()

        # Remove button definition from global settings
        for button_definition in self.global_settings_manager.global_settings_entity.button_definitions:
            if button_id == button_definition.button_id:
                self.global_settings_manager.remove_button_definition(button_definition)
                self.global_settings_manager.save_encoding_button_definitions()

    @Slot()
    def open_remove_button_definition_dialog(self):
        """
        Open a dialog to remove a button definition from global settings
        """
        self.remove_button_definition_dialog = RemoveButtonDefinitionDialog()
        self.remove_button_definition_dialog.connect_remove_button_to_slot(self.remove_button_definition)
        self.remove_button_definition_dialog.connect_clear_button_to_slot(
            self.open_confirm_clear_all_button_definitions_dialog)
        self.remove_button_definition_dialog.exec()

    @Slot()
    def open_confirm_clear_all_button_definitions_dialog(self):
        """
        Open a dialog to ask the user if they want to clear all the encoding button definitions
        (from global settings)
        """
        msg_box = QMessageBox()
        msg_box.setText("Are you sure you want to clear all button definitions?")
        msg_box.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        ret = msg_box.exec()
        self.clear_all_button_definitions(ret == QMessageBox.Yes)

    @Slot(bool)
    def clear_all_button_definitions(self, clear_definitions):
        """
        Clear all saved button definitions from global settings
        """
        button_definition_list = self.user_settings.button_definition_list.layout()

        if clear_definitions:
            while button_definition_list.count():
                element = button_definition_list.takeAt(0)
                if element and element.widget():
                    element.widget().deleteLater()
            self.global_settings_manager.global_settings_entity.button_definitions.clear()
            self.global_settings_manager.save_encoding_button_definitions()

    def open_settings_dialog(self, window_controller=None):
        """
        Creates the layout for the settings dialog in header menu and allows for settings to be changed

        Parameters:
            window_controller - reference to window controller if the window exists.

        """
        self.user_settings = UserSettingsDialog(self.global_settings_manager.global_settings_entity.button_definitions)
        self._window_controller = window_controller

        self.user_settings.connect_remove_button_to_slot(self.open_remove_button_definition_dialog)
        if window_controller:
            self.user_settings.connect_edit_button_to_slot(self.open_select_edit_button_dialog)
            self.user_settings.connect_cell_size_to_slot(window_controller.set_cell_size)
            self.user_settings.connect_maximum_size_to_slot(window_controller.set_maximum_width)
            self.user_settings.connect_padding_to_slot(window_controller.set_padding)
        else:
            self.user_settings.edit_button.setEnabled(False)

        self.user_settings.exec()

        width_text = self.user_settings.minimum_size_width_box.text()
        height_text = self.user_settings.minimum_size_height_box.text()
        if width_text != "" and height_text != "":
            table_cell_size = [int(width_text), int(height_text)]
            self.global_settings_manager.set_table_cell_size(table_cell_size)

        table_maximum_width = self.user_settings.maximum_width_text_box.text()
        if table_maximum_width != "":
            table_maximum_width = int(table_maximum_width)
            self.global_settings_manager.set_table_maximum_width(table_maximum_width)

        padding = self.user_settings.padding_text_box.text()
        if padding != "":
            padding = int(padding)
            self.global_settings_manager.set_table_padding(padding)

        # Saves the data to file.
        self.global_settings_manager.save_user_settings()
