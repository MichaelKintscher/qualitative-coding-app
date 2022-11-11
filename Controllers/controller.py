import sys
import time

from PySide6.QtCore import Slot, QMimeDatabase
from PySide6.QtMultimedia import QMediaFormat, QMediaPlayer
from PySide6.QtWidgets import QFileDialog, QDialog


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

        self.total_time_in_secs = 0
        self.curr_time_secs = 0
        self.curr_time_minutes = 0
        self.curr_time_hours = 0
        self._media_player.positionChanged.connect(self.get_video_time_total)

        self._window.table_panel.add_col_button.clicked.connect(self.add_col_to_encoding_table)
        self._window.table_panel.add_row_button.clicked.connect(self.add_row_to_encoding_table)

    @Slot()
    def add_col_to_encoding_table(self):
        """Command the table widget to add a column."""
        self._window.table_panel.table.add_column()

    @Slot()
    def add_row_to_encoding_table(self):
        """Command the table widget to add a row."""
        self._window.table_panel.table.add_row()

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
        frames = 0
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
        frames = ms * .024
        frames = int(frames)

        # This formats the time in the hr:min:sec:frame format.
        total_time_str = f"{hours_rounded_down:02d}:{minutes_rounded_down:02d}:{sec_rounded_down:02d}:{frames:02d}"

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
