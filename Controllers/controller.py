import sys

from PySide6.QtCore import Slot, QMimeDatabase, QByteArray
from PySide6.QtMultimedia import QMediaFormat, QMediaPlayer
from PySide6.QtWidgets import QFileDialog, QDialog, QMessageBox

import io
import csv


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

        self._window.table_panel.add_col_button.clicked.connect(self.add_col_to_encoding_table)
        self._window.table_panel.add_row_button.clicked.connect(self.add_row_to_encoding_table)

        self._window.connect_export_file_to_slot(self.save_to_file)

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
        file_dialog.saveFileContent(table_data_as_byte_array, "your_table_data.csv")
