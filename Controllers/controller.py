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
        self._media_player.setVideoOutput(self._window.get_video_widget())
        self._media_player.setAudioOutput(self._window.get_audio_widget())

        self._window.connect_load_video_to_slot(self.open_file_dialog)

        self._window.get_encoding_table_widget().connect_add_table_row_to_slot(self.add_row_to_encoding_table)
        self._window.get_encoding_table_widget().connect_add_table_col_to_slot(self.add_col_to_encoding_table)

    @Slot()
    def add_col_to_encoding_table(self):
        self._window.get_encoding_table_widget().add_column()

    @Slot()
    def add_row_to_encoding_table(self):
        """Add Row Button Logic"""
        self._window.get_encoding_table_widget().add_row()

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

        # Uses list of mime types to get filenames.
        for i, item in enumerate(mime_types):
            temp = ""
            temp = item.removeprefix("audio/")
            if temp == item:
                temp = item.removeprefix("video/")
            mime_types[i] = temp

        # Appends the correct file types to a new list based on the Mime Types list.
        filtered_types = []
        for i in mime_types:
            if i == "quicktime":
                filtered_types.append("QuickTime video (*.mov)")
            elif i == "mp4":
                filtered_types.append("MP4 video (*.mp4)")
            elif i == "x-msvideo":
                filtered_types.append("AVI video (*.avi)")
            else:
                continue

        # Appends .wmv and a default option that allows all files to be selected.
        filtered_types.append("WMV video (*.wmv)")
        filtered_types.append("All supported files (*.mov *.mp4 *avi *wmv)")
        file_dialog.setNameFilters(filtered_types)

        # This sets the defaulted displayed mime type to all supported files.
        default_mimetype = "All supported files (*.mov *.mp4 *avi *wmv)"
        file_dialog.selectNameFilter(default_mimetype)

        # This checks if a file to play has been selected.
        if file_dialog.exec() == QDialog.Accepted:
            url = file_dialog.selectedUrls()[0]
            self._media_player.setSource(url)
            self._media_player.play()
