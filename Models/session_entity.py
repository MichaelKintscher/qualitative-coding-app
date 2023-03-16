from PySide6.QtCore import Slot, QSettings
from PySide6.QtGui import QCloseEvent


class SessionEntity:
    """
    A data structure that holds all the data relevant to maintain session
    persistence.
    """

    def __init__(self):
        """
        Constructor - contains initial values for the session id, table name,
        table rows, table columns, table headers, and table data.
        """
        self.session_id = ""
        self.button_definitions = []
        self.table_name = ""
        self.table_row_count = 0
        self.table_col_count = 0
        self.table_headers = []
        self.table_data = []
