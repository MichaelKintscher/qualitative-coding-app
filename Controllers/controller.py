from PySide6.QtCore import Slot


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
        self.window = window
        self.window.get_encoding_table_widget().connect_add_table_row_to_slot(self.add_row_to_encoding_table)

    @Slot()
    def add_row_to_encoding_table(self):
        """Add Row Button Logic"""
        self.window.get_encoding_table_widget().add_row()

