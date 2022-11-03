import sys

from PySide6.QtCore import Slot
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
        mp4_video_file = 'video/mp4'

        # Opens the file browser, doesn't need any arguments as the window calls this.
        file_dialog = QFileDialog()

        # This gets the mime_types for the specific system and sets a filter.
        is_windows = sys.platform == 'win32'
        mime_types = get_supported_mime_types()

        # Adds AVI and MP4 if they were not supported.
        if is_windows and avi_video_file not in mime_types:
            mime_types.append(avi_video_file)
        elif mp4_video_file not in mime_types:
            mime_types.append(mp4_video_file)
        file_dialog.setMimeTypeFilters(mime_types)

        # This checks if a file to play has been selected.
        if file_dialog.exec() == QDialog.Accepted:
            url = file_dialog.selectedUrls()[0]
            self._media_player.setSource(url)
            self._media_player.play()
