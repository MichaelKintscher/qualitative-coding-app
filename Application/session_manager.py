from PySide6.QtCore import Slot, QSettings
from PySide6.QtGui import QCloseEvent

#from Models.session_entity import SessionEntity


class SessionManager:
    def __init__(self):
        #self.session_entity = SessionEntity
        self.session_id = ""
        self.table_name = ""
        self.table_row = 0
        self.table_col = 0
        self.table_headers = []
        self.table_data = []

    def set_session_id(self, session_id):
        self.session_id = session_id

    def set_table_name(self, table_name):
        self.table_name = table_name

        settings = QSettings()
        settings.beginGroup(self.session_id)
        settings.beginGroup("encoding-table-panel")  # creates bin within session_id bin

        settings.setValue("title", self.table_name)

        # need to leave the bin

        settings.endGroup()  # encoding-table-panel
        settings.endGroup()  # session-id

    def set_table_rows(self, row_count):
        self.table_row = row_count

    def set_table_cols(self, col_count):
        self.table_col = col_count

    def set_table_headers(self, headers):
        self.table_headers = headers

    def set_table_data(self, data):
        self.table_data = data
