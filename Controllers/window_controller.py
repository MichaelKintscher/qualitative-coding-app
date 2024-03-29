import io
import csv
import math
import sys

from PySide6.QtCore import Slot, QMimeDatabase, QByteArray
from PySide6.QtGui import QFontMetrics, QKeySequence
from PySide6.QtMultimedia import QMediaFormat, QMediaPlayer
from PySide6.QtWidgets import QFileDialog, QDialog, QStyle, QInputDialog, QLineEdit, QPushButton, QTableWidgetItem, \
    QMessageBox, QWidget

from Application.button_manager import ButtonManager
from View.button_definition_list_element import ButtonDefinitionListElement
from View.edit_coding_assistance_button_dialog import EditCodingAssistanceButtonDialog
from View.load_coding_assistance_button_dialog import LoadCodingAssistanceButtonDialog
from View.remove_button_definition_dialog import RemoveButtonDefinitionDialog
from View.select_edit_button_dialog import SelectEditButtonDialog
from View.user_settings_dialog import UserSettingsDialog
from View.add_coding_assistance_button_dialog import AddCodingAssistanceButtonDialog
from View.delete_coding_assistance_button_dialog import DeleteCodingAssistanceButtonDialog

from Models.button_definition_entity import ButtonDefinitionEntity

from Controllers.project_management_controller import ProjectManagementController


def get_supported_mime_types():
    """
    get_supported_mime_types() - This returns a list of supported
    mime types for the specific OS. It is used to set a filter on files so
    only media files can be played.

    Return:
        result - A list of all supported media file types
    """
    result = []
    for f in QMediaFormat().supportedFileFormats(QMediaFormat.Decode):
        mime_type = QMediaFormat(f).mimeType()
        result.append(mime_type.name())
    return result


class WindowController:
    """
    The WindowController responds to input events from the Window. The Controller
    handles the main logic of the application.
    """
    DEFAULT_FRAMES_PER_SECOND = 30

    def __init__(self, window, global_settings_manager, user_settings_controller):
        """
        Constructor - Initializes the Controller instance.

        Parameters:
            window (MainWindow): the main Window of the application
            global_settings_manager - reference to the global settings manager.
            user_settings_controller - reference to the user settings controller
        """
        self._window = window

        self.global_settings_manager = global_settings_manager
        self.user_settings_controller = user_settings_controller
        self.button_manager = ButtonManager()

        self._media_player = QMediaPlayer()
        self._media_player.setVideoOutput(
            self._window.media_panel.video_widget)
        self._media_player.setAudioOutput(
            self._window.media_panel.audio_widget)

        self._window.connect_load_video_to_slot(self.open_file_dialog)
        self._window.connect_settings_to_slot(self.open_settings_dialog)

        self._window.table_panel.change_font_dropDown.activated.connect(
            self.change_font_of_encoding_table)

        self._window.table_panel.table.horizontalHeader(
        ).sectionDoubleClicked.connect(self.edit_header)
        self._window.table_panel.table.horizontalHeader(
        ).line.editingFinished.connect(self.done_editing)

        self._window.table_panel.title.textChanged.connect(self.resize_to_content)

        self._window.media_panel.media_control_panel.play_pause_button.clicked.connect(
            self.play_video)

        self._window.media_panel.scalable_scrubber_bar.scrubber_bar.sliderMoved.connect(
            self.update_video_on_progres_bar_movement)

        self._media_player.positionChanged.connect(self.update_progress_bar_on_video_position_changed)
        self._media_player.durationChanged.connect(self.on_video_duration_changed)

        self._window.media_panel.media_control_panel. \
            playback_speed_combo_box.currentIndexChanged.connect(
                self.set_playback_speed)

        # Holds the time for the loaded video in ms.
        self.current_time = 0
        self._media_player.positionChanged.connect(self.get_video_time_total)

        self._window.table_panel.add_col_button.clicked.connect(self.add_col_to_encoding_table)
        self._window.table_panel.add_row_button.clicked.connect(self.add_row_to_encoding_table)
        self._window.table_panel.delete_col_button.clicked.connect(self.del_current_column)
        self._window.table_panel.delete_row_button.clicked.connect(self.del_current_row)

        self._window.connect_export_file_to_slot(self.save_to_file)

        self._window.coding_assistance_panel.button_panel.connect_add_button_to_slot(self.open_add_coding_assistance_button_dialog)
        self._window.coding_assistance_panel.button_panel.connect_delete_button_to_slot(self.open_delete_coding_assistance_button_dialog)

        # Resizes the title bar of the encoding table, this is triggered
        #   manually here since the slot was not connected to the encoding
        #   table when its title was initialized.
        self.resize_to_content()

    @Slot()
    def add_col_to_encoding_table(self):
        """ Command the table widget to add a column. """
        self._window.table_panel.table.add_column()

    @Slot()
    def add_row_to_encoding_table(self):
        """ Command the table widget to add a row. """
        self._window.table_panel.table.add_row()

    @Slot()
    def del_current_column(self):
        """ Command the table widget to delete current selected column"""
        self._window.table_panel.table.del_column()

    @Slot()
    def del_current_row(self):
        """ Command the table widget to delete current selected row"""
        self._window.table_panel.table.del_row()

    @Slot()
    def change_font_of_encoding_table(self):
        """
        Get selected item from font dropdown.
        Command table cells font to update to selected font size.
        """
        selected_font = int(
            self._window.table_panel.change_font_dropDown.currentText())
        self._window.table_panel.table.change_font(selected_font)

    @Slot()
    def edit_header(self, section):
        """
        Commands QLineEdit item to become editable.

        Parameters:
            section: keeps track of which column header is being edited.
        """
        self._window.table_panel.table.edit_header(section)

    def establish_table_title(self, table_title):
        """
        Opens an input dialog box to request an initial title for the encoding
        table of the session. Then, sets the initial title to the user-response.
        """
        self._window.table_panel.title.setText(table_title)
        self.resize_to_content()

    @Slot()
    def done_editing(self):
        """Commands the table widget to update header label to the text entered in the QLineEdit item"""
        self._window.table_panel.table.done_editing()

    @Slot(int)
    def on_video_duration_changed(self, new_duration):
        """
        Initialize the scrubbing bars according to the new duration of the
        media player. Triggered when a new video is loaded.

        Parameters:
            new_duration - current duration of the video.
        """
        self._window.media_panel.scalable_scrubber_bar.initialize(new_duration)

    @Slot()
    def get_video_time_total(self):
        """
        get_video_time_total() - Slot function that will act as a handler whenever a video
        is loaded in order to get the time in hr, mins, sec, frames.
        """
        # Get the total time of the video in milliseconds.
        total_in_ms = self._media_player.duration()
        self.current_time = self._media_player.position()

        # This convert to seconds, minutes, hours, and frames
        # and rounds down to the nearest value.
        sec_rounded_down = 0
        minutes_rounded_down = 0
        hours_rounded_down = 0
        total_time_str = ""

        if total_in_ms > 1000:
            sec = total_in_ms / 1000
            sec_rounded_down = int(sec)
        if sec_rounded_down > 60:
            minutes = sec_rounded_down / 60
            minutes_rounded_down = int(minutes)
            sec_rounded_down -= (minutes_rounded_down * 60)
        if minutes_rounded_down > 60:
            hours = minutes_rounded_down / 60
            hours_rounded_down = int(hours)
            minutes_rounded_down -= (hours_rounded_down * 60)
        ms = total_in_ms % 1000

        # This formats the time in the hr:min:sec:frame format.
        total_time_str = f"{hours_rounded_down:02d}:{minutes_rounded_down:02d}:{sec_rounded_down:02d}"

        # This gets the current time in seconds.
        current_seconds = (self.current_time / 1000) % 60
        current_seconds = int(current_seconds)
        current_minutes = (self.current_time / (1000 * 60)) % 60
        current_minutes = int(current_minutes)
        current_hours = (self.current_time / (1000 * 60 * 60)) % 24
        current_hours = int(current_hours)

        # Formats the time displaying current time/ total time
        # and then sets the text label in the media control panel.
        time_str_formatted = f"{current_hours:02d}:{current_minutes:02d}:{current_seconds:02d}" \
                             f"/{total_time_str}"
        self._window.media_panel.media_control_panel.time_stamp.setText(time_str_formatted)

    @Slot()
    def open_file_dialog(self):
        """
        load_video_handler() - Slot function that will act as a handler whenever the
        load video button is clicked.
        """
        # Variables for AVI and MP4 video files.
        avi_video_file = "video/x-msvideo"
        mp4_video_file = "video/mp4"

        # Opens the file browser, doesn't need any arguments as the window calls this.
        file_dialog = QFileDialog()

        # Opens file browser with qt specific file browser instead of os specific.
        file_dialog.setOption(QFileDialog.DontUseNativeDialog)

        # This gets the mime_types for the specific system and sets a filter.
        is_windows = sys.platform == 'win32'
        mime_types = get_supported_mime_types()

        # Adds AVI and MP4 if they were not supported.
        if is_windows and avi_video_file not in mime_types:
            mime_types.append(avi_video_file)
        elif mp4_video_file not in mime_types:
            mime_types.append(mp4_video_file)

        # Store all the supported mime type glob patterns into a single list.
        mime_db = QMimeDatabase()
        glob_pattern_lists = []
        for mime_type in mime_types:
            mime_name = mime_db.mimeTypeForName(mime_type)
            glob_pattern_lists.append(mime_name.globPatterns())

        # Set the QFileDialog mime type filters.
        file_dialog.setMimeTypeFilters(mime_types)

        # Add an "all supported types" filter and make it the default.
        glob_patterns_list = [
            item for sublist in glob_pattern_lists for item in sublist]
        glob_patterns_str = " ".join(glob_patterns_list)
        all_supported_types = f"All supported formats {glob_patterns_str}"
        name_filters = file_dialog.nameFilters()
        name_filters.insert(0, all_supported_types)
        file_dialog.setNameFilters(name_filters)
        file_dialog.selectNameFilter(all_supported_types)

        # This checks if a file to play has been selected.
        if file_dialog.exec() == QDialog.Accepted:
            url = file_dialog.selectedUrls()[0]
            self._media_player.setSource(url)
            self._media_player.play()
            self.toggle_play_pause_icon()

    @Slot()
    def open_settings_dialog(self):
        """
        Creates the layout for the settings dialog in header menu and allows for settings to be changed
        """
        self.user_settings_controller.open_settings_dialog(self)

    @Slot()
    def save_to_file(self):
        """
        save_to_file() - Slot function that will act as a handler whenever the
        Save table data button is clicked.
        """
        # Opens the file browser on the main window.
        file_dialog = QFileDialog(self._window)

        output = io.StringIO()
        csv_writer = csv.writer(output, delimiter=",", quoting=csv.QUOTE_NONNUMERIC)

        # Traverse over the table data and format data in CSV style.
        num_rows = self._window.table_panel.table.rowCount()
        num_columns = self._window.table_panel.table.columnCount()
        for y in range(num_rows):
            table_row = []
            for x in range(num_columns):
                item = self._window.table_panel.table.item(y, x)
                if item is not None:
                    single_entity_of_table = item.text()
                    table_row.append(single_entity_of_table)
                else:
                    table_row.append("")
            csv_writer.writerow(table_row)

        # Convert to a byte array and open file browser to save.
        table_data_as_byte_array = QByteArray(output.getvalue())
        title_name = self._window.table_panel.title.text()
        if title_name == "":
            file_dialog.saveFileContent(table_data_as_byte_array, "your_table_data.csv")
        else:
            file_dialog.saveFileContent(table_data_as_byte_array, title_name + ".csv")

    @Slot()
    def play_video(self):
        """ Command a video to change the state to play and pause when clicked. """
        if self._media_player.playbackState() == QMediaPlayer.PlayingState:
            self._media_player.pause()
        else:
            self._media_player.play()
        self.toggle_play_pause_icon()

    @Slot()
    def resize_to_content(self):
        """ Update the width of the table title label to its title content width. """
        title = self._window.table_panel.title
        text = title.text()
        font_metrics = QFontMetrics(title.font())

        padding = 25
        title.setFixedWidth(font_metrics.horizontalAdvance(text) + padding)

    @Slot()
    def set_playback_speed(self):
        """
        Updates the playback speed of the multimedia based on the data of the
        playback speed combo box.
        """
        current_playback_speed = self._window.media_panel.media_control_panel.playback_speed_combo_box.currentData()
        self._media_player.setPlaybackRate(current_playback_speed)

    @Slot(int)
    def update_progress_bar_on_video_position_changed(self, position):
        """
        Sets the value of the progress bar sliders based on the new position of
        the media player. Triggered as the video progresses.

        Parameters:
            position - current position of the video
        """
        self._window.media_panel.scalable_scrubber_bar.progress_bar.setValue(position)
        self._window.media_panel.scalable_scrubber_bar.scrubber_bar.setValue(position)

    @Slot()
    def set_cell_size(self):
        """
        Takes input from the settings dialog and calls the set_cell_size function in the encoding table.
        """
        width_text = self.user_settings_controller.get_dialog().minimum_size_width_box.text()
        height_text = self.user_settings_controller.get_dialog().minimum_size_height_box.text()
        if width_text != "":
            width = int(width_text)
            self._window.table_panel.table.set_table_width(width)
        if height_text != "":
            height = int(height_text)
            self._window.table_panel.table.set_table_height(height)

    @Slot()
    def set_maximum_width(self):
        """
        Takes input from the settings dialog and calls the set_maximum_width function in the encoding table.
        """
        width_text = self.user_settings_controller.get_dialog().maximum_width_text_box.text()
        try:
            width = int(width_text)
            self._window.table_panel.table.set_maximum_width(width)
        except ValueError:
            pass

    @Slot()
    def set_padding(self):
        """
        Takes input from the settings dialog and calls the set_padding function in encoding_table.py
        """
        padding = self.user_settings_controller.get_dialog().padding_text_box.text()
        self._window.table_panel.table.set_padding(padding)

    @Slot()
    def set_playback_speed(self):
        """
        Updates the playback speed of the multimedia based on the data of the
        playback speed combo box.
        """
        current_playback_speed = self._window.media_panel.media_control_panel.playback_speed_combo_box.currentData()
        self._media_player.setPlaybackRate(current_playback_speed)

    @Slot(int)
    def update_video_on_progres_bar_movement(self, new_position):
        """
        Commands the video player to set the position state based on the new
        value of the progress bar slider. Triggered when the user slides
        the progress bar.

        Parameters:
            new_position - current position of progress bar
        """
        # Only set the position of the media player if a video has been loaded.
        if self._media_player.source().url():
            self._media_player.setPosition(new_position)

    @Slot()
    def toggle_play_pause_icon(self):
        """ Toggles the icon of the play/pause button. """
        button = self._window.media_panel.media_control_panel.play_pause_button
        if self._media_player.playbackState() == QMediaPlayer.PlayingState:
            button.setIcon(button.style().standardIcon(QStyle.SP_MediaPause))
        else:
            button.setIcon(button.style().standardIcon(QStyle.SP_MediaPlay))

    @Slot()
    def open_add_coding_assistance_button_dialog(self):
        """
        Open a dialog to create a new Coding Assistance Button
        """
        self.add_coding_assistance_button_dialog = AddCodingAssistanceButtonDialog(self._window.table_panel.table)
        self.add_coding_assistance_button_dialog.connect_create_button_to_slot(
            self.open_save_coding_assistance_button_dialog,
            self.add_coding_assistance_button_dialog)
        self.add_coding_assistance_button_dialog.connect_load_button_to_slot(
            self.open_load_coding_assistance_button_dialog,
            self.add_coding_assistance_button_dialog)
        self.add_coding_assistance_button_dialog.exec()

    @Slot()
    def open_delete_coding_assistance_button_dialog(self):
        """
        Open a dialog to create a new Coding Assistance Button
        """
        self.delete_coding_assistance_button_dialog = DeleteCodingAssistanceButtonDialog()
        self.delete_coding_assistance_button_dialog.connect_delete_button_to_slot(
            self.delete_coding_assistance_button,
            self.delete_coding_assistance_button_dialog)
        self.delete_coding_assistance_button_dialog.exec()

    @Slot()
    def open_load_coding_assistance_button_dialog(self):
        """
        Open a dialog to load a Coding Assistance Button
        """
        self.load_coding_assistance_button_dialog = LoadCodingAssistanceButtonDialog(
            self.global_settings_manager.global_settings_entity.button_definitions)
        self.load_coding_assistance_button_dialog.connect_load_button_to_slot(
            ProjectManagementController.make_lambda(
            self.load_coding_assistance_button, self.load_coding_assistance_button_dialog.radio_buttons),
            self.load_coding_assistance_button_dialog)
        self.load_coding_assistance_button_dialog.exec()

    @Slot()
    def open_save_coding_assistance_button_dialog(self):
        """
        Open a dialog to ask the user if they want to save the encoding button definition
        (to global settings)
        """
        msg_box = QMessageBox()
        msg_box.setText("Do you want to save this button definition?")
        msg_box.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        ret = msg_box.exec()
        self.create_coding_assistance_button(ret == QMessageBox.Yes)

    @Slot(bool)
    def create_coding_assistance_button(self, save_button):
        """
        Add a button to the Coding Assistance Panel. This method may also save
        the created button definition to global storage.

        Parameters:
            save_button - Flag indicating whether the created button definition
            is saved to global storage.
        """
        button_name = self.add_coding_assistance_button_dialog.apply_text_field.text()
        button_hotkey = self.add_coding_assistance_button_dialog.hotkey_field.text()
        button_exists = False

        data = []
        for text in self.add_coding_assistance_button_dialog.dynamic_line_edits:
            data.append(text.text())

        saved_button_definitions = self.global_settings_manager.global_settings_entity.button_definitions
        hotkeys = self.button_manager.get_hotkeys()
        new_button = QPushButton(button_name)
        new_button.setShortcut(QKeySequence(button_hotkey))
        new_button_definition = ButtonDefinitionEntity(button_name, data)

        if not hotkeys:
            for button_definition in saved_button_definitions:
                if button_definition.button_id == button_name:
                    button_exists = True
                    break
            if save_button and not button_exists:
                self.global_settings_manager.add_button_definition(new_button_definition)

            self.add_coding_assistance_button_dialog.error_label.setText("")
            self._window.coding_assistance_panel.button_panel.create_coding_assistance_button(new_button)
            new_button.clicked.connect(ProjectManagementController.make_lambda(
                self.dynamic_button_click, new_button_definition))

            self.button_manager.add_button_definition(button_name, new_button_definition)
            self.button_manager.add_button_hotkey(button_name, button_hotkey)
        else:
            if button_hotkey in hotkeys:
                self.add_coding_assistance_button_dialog.error_label.setText("This hotkey is already being used!")
            else:
                for button_definition in saved_button_definitions:
                    if button_definition.button_id == button_name:
                        button_exists = True
                        break
                if save_button and not button_exists:
                    self.global_settings_manager.add_button_definition(new_button_definition)

                self.add_coding_assistance_button_dialog.error_label.setText("")
                self._window.coding_assistance_panel.button_panel.create_coding_assistance_button(new_button)
                new_button.clicked.connect(ProjectManagementController.make_lambda(
                    self.dynamic_button_click, new_button_definition))

                self.button_manager.add_button_definition(button_name, new_button_definition)
                self.button_manager.add_button_hotkey(button_name, button_hotkey)

    def create_button(self, hotkey, button_definition):
        """
        Creates and establishes an encoding button. This method adds the button
        to the button panel.

        Parameters:
            hotkey - hotkey of button
            button_definition - definition of button
        """
        button_name = button_definition.button_id
        button = QPushButton(button_name)
        button.setShortcut(QKeySequence(hotkey))
        self._window.coding_assistance_panel.button_panel.create_coding_assistance_button(button)
        button.clicked.connect(ProjectManagementController.make_lambda(
            self.dynamic_button_click, button_definition))
        self.button_manager.add_button_definition(button_name, button_definition)
        self.button_manager.add_button_hotkey(button_name, hotkey)

    @Slot()
    def load_coding_assistance_button(self, radio_buttons):
        """
        Load selected buttons to the Coding Assistance Panel

        Parameters:
            radio_buttons - A list of radio buttons created in the Load Button Dialog
        """
        hotkeys = self.button_manager.get_hotkeys()

        hotkey = self.load_coding_assistance_button_dialog.hotkey_textfield.text()
        for i, radio_button in enumerate(radio_buttons):
            if radio_button.isChecked():
                button_definition = self.global_settings_manager.global_settings_entity.button_definitions[i]
        button_id = button_definition.button_id
        new_button = QPushButton(button_id)
        new_button.setShortcut(QKeySequence(hotkey))

        if not hotkeys:
            self._window.coding_assistance_panel.button_panel.create_coding_assistance_button(new_button)
            new_button.clicked.connect(
                ProjectManagementController.make_lambda(self.dynamic_button_click, button_definition))

            self.button_manager.add_button_definition(button_id, button_definition)
            self.button_manager.add_button_hotkey(button_id, hotkey)
        else:
            if hotkey in hotkeys:
                self.load_coding_assistance_button_dialog.error_label.setText("This hotkey is already being used!")
            else:
                self._window.coding_assistance_panel.button_panel.create_coding_assistance_button(new_button)
                new_button.clicked.connect(
                    ProjectManagementController.make_lambda(self.dynamic_button_click, button_definition))

                self.button_manager.add_button_definition(button_id, button_definition)
                self.button_manager.add_button_hotkey(button_id, hotkey)

    @Slot()
    def delete_coding_assistance_button(self):
        """
        Delete a button from the Coding Assistance Panel
        """
        button_id = self.delete_coding_assistance_button_dialog.button_name_textbox.text()
        self._window.coding_assistance_panel.button_panel.delete_coding_assistance_button(button_id)
        self.button_manager.remove_button_definition(button_id)
        self.button_manager.remove_button_hotkey(button_id)

    @Slot(ButtonDefinitionEntity)
    def dynamic_button_click(self, button_definition):
        """
        Add button data to table when clicked

        Parameters:
            button_definition - An instance of ButtonDefinition
        """
        if not self._media_player.hasVideo():
            return

        video_timestamp = self._window.media_panel.media_control_panel.time_stamp.text()
        split = video_timestamp.split("/")
        video_timestamp = split[0]
        timestamp_text = QTableWidgetItem(video_timestamp)
        for row in range(self._window.table_panel.table.rowCount()):
            column = 0
            cell = self._window.table_panel.table.item(row, column)
            if not cell:
                self._window.table_panel.table.setItem(row, column, timestamp_text)
                column = 1
                data = 0
                while column <= self._window.table_panel.table.columnCount():
                    insert_text = QTableWidgetItem(button_definition.data[data])
                    self._window.table_panel.table.setItem(row, column, insert_text)
                    column += 1
                    data += 1
                return
