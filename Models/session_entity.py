from PySide6.QtCore import Slot, QSettings
from PySide6.QtGui import QCloseEvent


class SessionEntity:
    def __init__(self):
        self.session_id = ""
        self.table_name = ""
        self.table_row = 0
        self.table_col = 0
        self.table_headers = []
        self.table_data = []


