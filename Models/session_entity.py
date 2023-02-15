from PySide6.QtCore import Slot, QSettings
from PySide6.QtGui import QCloseEvent


class SessionEntity:
    """
    A data structure that holds all the data relevant to maintain table
    persistence. It is instantiated in the TableManager.
    """
    def __init__(self):
        """
        Constructor - contains initial values for the session id, table name,
        table rows, table columns, table headers, and table data.
        """
        self.session_id = ""
        self.table_name = ""
        self.table_row = 0
        self.table_col = 0
        self.table_headers = []
        self.table_data = []


