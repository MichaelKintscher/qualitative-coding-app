import sys

from PySide6.QtCore import Slot, QMimeDatabase
from PySide6.QtMultimedia import QMediaFormat, QMediaPlayer
from PySide6.QtWidgets import *

from View.user_settings_dialog import UserSettingsDialog


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


class Controller:
    """
    The Controller responds to input events from the View. The Controller
    interacts with the application Manager or with the Qt framework in order to
    perform the appropriate response.
    """

    def __init__(self, window):
        """
        Constructor - Initializes the Controller instance.

        Parameters:
            window (MainWindow): the main Window of the application
        """
        self._window = window

        self._media_player = QMediaPlayer()
        self._media_player.setVideoOutput(self._window.media_panel.video_widget)
        self._media_player.setAudioOutput(self._window.media_panel.audio_widget)

        self._window.connect_load_video_to_slot(self.open_file_dialog)
        self._window.connect_settings_to_slot(self.open_settings_dialog)

        self._window.table_panel.add_col_button.clicked.connect(self.add_col_to_encoding_table)
        self._window.table_panel.add_row_button.clicked.connect(self.add_row_to_encoding_table)

        self._window.media_panel.progress_bar_slider.sliderMoved.connect(self.set_position)

        self._media_player.positionChanged.connect(self.position_changed)
        self._media_player.durationChanged.connect(self.duration_changed)
        
        self._window.media_panel.media_control_panel. \
            playback_speed_combo_box.currentIndexChanged.connect(self.set_playback_speed)

    @Slot()
    def add_col_to_encoding_table(self):
        """
        Command the table widget to add a column.
        """
        self._window.table_panel.table.add_column()

    @Slot()
    def add_row_to_encoding_table(self):
        """
        Command the table widget to add a row.
        """
        self._window.table_panel.table.add_row()

    @Slot()
    def duration_changed(self):
        """
        Sets the range of the progress bar when the
        duration of the media player changes.
        """
        duration = self._media_player.duration()
        self._window.media_panel.progress_bar_slider.setRange(0, duration)

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
        glob_patterns_list = [item for sublist in glob_pattern_lists for item in sublist]
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
