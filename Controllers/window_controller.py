import io
import csv
import sys

from datetime import datetime

from PySide6.QtCore import Slot, QMimeDatabase, QByteArray
from PySide6.QtGui import QFontMetrics, QKeySequence
from PySide6.QtMultimedia import QMediaFormat, QMediaPlayer
from PySide6.QtWidgets import QFileDialog, QDialog, QStyle, QInputDialog, QLineEdit, QMessageBox, QPushButton, QTableWidgetItem

from View.user_settings_dialog import UserSettingsDialog
from View.add_coding_assistance_button_dialog import AddCodingAssistanceButtonDialog
from View.delete_coding_assistance_button_dialog import DeleteCodingAssistanceButtonDialog

from Application.manager import Manager
from Application.button_definition import ButtonDefinition


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

    def __init__(self, window):
        """
        Constructor - Initializes the Controller instance.

        Parameters:
            window (MainWindow): the main Window of the application
        """
        self._window = window

        self._manager = Manager()

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

        self._window.media_panel.progress_bar_slider.sliderMoved.connect(
            self.set_position)

        self._media_player.positionChanged.connect(self.position_changed)
        self._media_player.durationChanged.connect(self.duration_changed)

        self._window.media_panel.media_control_panel. \
            playback_speed_combo_box.currentIndexChanged.connect(
                self.set_playback_speed)

        self.total_time_in_secs = 0
        self.curr_time_secs = 0
        self.curr_time_minutes = 0
        self.curr_time_hours = 0
        self._media_player.positionChanged.connect(self.get_video_time_total)

        self._window.table_panel.add_col_button.clicked.connect(self.add_col_to_encoding_table)
        self._window.table_panel.add_row_button.clicked.connect(self.add_row_to_encoding_table)

        self._window.media_panel.media_control_panel.input_start_time.editingFinished.connect(self.change_scrub_start)
        self._window.media_panel.media_control_panel.input_end_time.editingFinished.connect(self.change_scrub_end)

        self._window.connect_export_file_to_slot(self.save_to_file)

        self._window.coding_assistance_panel.button_panel.connect_add_button_to_slot(self.open_add_coding_assistance_button_dialog)
        self._window.coding_assistance_panel.button_panel.connect_delete_button_to_slot(self.open_delete_coding_assistance_button_dialog)
        
        if self._window.session_id == "New Session":
            self.establish_table_title()

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

    def establish_table_title(self):
        """
        Opens an input dialog box to request an initial title for the encoding
        table of the session. Then, sets the initial title to the user-response.
        """
        text, ok = QInputDialog.getText(self._window, "Encoding Table Title Name",
                                        "Encoding Table Title:", QLineEdit.Normal, "")
        if ok and text:
            self._window.table_panel.title.setText(text)
            self.resize_to_content()

    @Slot()
    def done_editing(self):
        """Commands the table widget to update header label to the text entered in the QLineEdit item"""
        self._window.table_panel.table.done_editing()

    def duration_changed(self):
        """
        Sets the range of the progress bar when the
        duration of the media player changes.
        """
        duration = self._media_player.duration()
        self._window.media_panel.progress_bar_slider.setRange(0, duration)

    @Slot()
    def get_video_time_total(self):
        """
        get_video_time_total() - Slot function that will act as a handler whenever a video
        is loaded in order to get the time in hr, mins, sec, frames.
        """
        # Get the total time of the video in milliseconds.
        total_in_ms = self._media_player.duration()
        current_time = self._media_player.position()

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
        temp = self.total_time_in_secs
        current_time = current_time - (1000 * self.total_time_in_secs)
        if current_time > 1000:
            self.total_time_in_secs += 1
            self.curr_time_secs += 1
        if self.curr_time_secs > 60:
            self.curr_time_secs = 0
            self.curr_time_minutes += 1
        if self.curr_time_minutes > 60:
            self.curr_time_minutes = 0
            self.curr_time_hours += 1

        # Formats the time displaying current time/ total time
        # and then sets the text label in the media control panel.
        time_str_formatted = f"Time: {self.curr_time_hours:02d}:{self.curr_time_minutes:02d}:{self.curr_time_secs:02d}" \
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
    def open_settings_dialog(self):
        """
        Creates the layout for the settings dialog in header menu and allows for settings to be changed
        """
        self.user_settings = UserSettingsDialog()
        self.user_settings.connect_cell_size_to_slot(self.set_cell_size)
        self.user_settings.connect_maximum_size_to_slot(self.set_maximum_width)
        self.user_settings.connect_padding_to_slot(self.set_padding)
        self.user_settings.exec()

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

    @Slot()
    def position_changed(self):
        """
        Sets the value of the progress bar slider based
        on the position of the media player.
        """
        position = self._media_player.position()
        self._window.media_panel.progress_bar_slider.setValue(position)

    @Slot()
    def set_cell_size(self):
        """
        Takes input from the settings dialog and calls the set_cell_size function in the encoding table.
        """
        width_text = self.user_settings.minimum_size_width_box.text()
        height_text = self.user_settings.minimum_size_height_box.text()
        try:
            width = int(width_text)
            height = int(height_text)
            self._window.table_panel.table.set_cell_size(width, height)
        except ValueError:
            pass

    @Slot()
    def set_maximum_width(self):
        """
        Takes input from the settings dialog and calls the set_maximum_width function in the encoding table.
        """
        width_text = self.user_settings.maximum_width_text_box.text()
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
        padding = self.user_settings.padding_text_box.text()
        self._window.table_panel.table.set_padding(padding)

    @Slot()
    def set_playback_speed(self):
        """
        Updates the playback speed of the multimedia based on the data of the
        playback speed combo box.
        """
        current_playback_speed = self._window.media_panel.media_control_panel.playback_speed_combo_box.currentData()
        self._media_player.setPlaybackRate(current_playback_speed)

    @Slot()
    def set_position(self, position):
        """
        Commands the video player to set the position state
        based on the value of the progress bar slider.
        """
        self._media_player.setPosition(position)

    @Slot()
    def toggle_play_pause_icon(self):
        """ Toggles the icon of the play/pause button. """
        button = self._window.media_panel.media_control_panel.play_pause_button
        if self._media_player.playbackState() == QMediaPlayer.PlayingState:
            button.setIcon(button.style().standardIcon(QStyle.SP_MediaPause))
        else:
            button.setIcon(button.style().standardIcon(QStyle.SP_MediaPlay))

    @Slot()
    def change_scrub_start(self):
        """
        Changes the start position of the scrubbing bar.
        """
        str_start_time = self._window.media_panel.media_control_panel.input_start_time.text()
        int_start_time = int(str_start_time) * 1000
        self._window.media_panel.progress_bar_slider.setMinimum(int_start_time)

    @Slot()
    def change_scrub_end(self):
        """
        Changes the end position of the scrubbing bar.
        """
        str_end_time = self._window.media_panel.media_control_panel.input_end_time.text()
        int_end_time = int(str_end_time) * 1000
        self._window.media_panel.progress_bar_slider.setMaximum(int_end_time)

    def open_add_coding_assistance_button_dialog(self):
        """Open a dialog to create a new Coding Assistance Button"""
        self.add_coding_assistance_button_dialog = AddCodingAssistanceButtonDialog()
        self.add_coding_assistance_button_dialog.connect_create_button_to_slot(self.create_coding_assistance_button)
        self.add_coding_assistance_button_dialog.exec()

    def open_delete_coding_assistance_button_dialog(self):
        """Open a dialog to create a new Coding Assistance Button"""
        self.delete_coding_assistance_button_dialog = DeleteCodingAssistanceButtonDialog()
        self.delete_coding_assistance_button_dialog.connect_delete_button_to_slot(self.delete_coding_assistance_button)
        self.delete_coding_assistance_button_dialog.exec()

    @Slot()
    def create_coding_assistance_button(self):
        """Add a button to the Coding Assistance Panel"""

        button_name = self.add_coding_assistance_button_dialog.apply_text_field.text()
        button_hotkey = self.add_coding_assistance_button_dialog.hotkey_field.text()
        new_button = QPushButton(button_name)
        new_button.setObjectName(button_name)
        new_button.setShortcut(QKeySequence(button_hotkey))
        new_button_definition = ButtonDefinition(new_button, button_name, button_hotkey)

        if not self._manager.hotkey_list:
            self._manager.hotkey_list.append(button_hotkey)
            self.add_coding_assistance_button_dialog.error_label.setText("")
            self._window.coding_assistance_panel.button_panel.create_coding_assistance_button(new_button_definition)
            self._manager.coding_assistance_button_list.append(new_button_definition)
            new_button.clicked.connect(self.dynamic_button_click)
        else:
            check = self._manager.hotkey_list.count(button_hotkey)
            if check > 0:
                self.add_coding_assistance_button_dialog.error_label.setText("This hotkey is already being used!")
            else:
                self._manager.hotkey_list.append(button_hotkey)
                self.add_coding_assistance_button_dialog.error_label.setText("")
                self._window.coding_assistance_panel.button_panel.create_coding_assistance_button(new_button_definition)
                self._manager.coding_assistance_button_list.append(new_button_definition)

    @Slot()
    def delete_coding_assistance_button(self):
        """Delete a button from the Coding Assistance Panel"""
        check_button_name = self.delete_coding_assistance_button_dialog.button_name_textbox.text()
        for button_definition in self._manager.coding_assistance_button_list:
            if check_button_name == button_definition.button_id:
                if button_definition.hotkey in self._manager.hotkey_list:
                    self._manager.hotkey_list.remove(button_definition.hotkey)
                self._window.coding_assistance_panel.button_panel.delete_coding_assistance_button(button_definition)

    def dynamic_button_click(self):
        """Add dummy data to table"""
        date_time = datetime.now()
        dt_string = date_time.strftime("%d/%m/%Y %H:%M:%S")

        column = 0
        for row in range(self._window.table_panel.table.rowCount()):
            cell = self._window.table_panel.table.item(row, column)
            if not cell:
                text = QTableWidgetItem(dt_string)
                self._window.table_panel.table.setItem(row, column, text)
                return
