from PySide6.QtCore import Slot, QSettings
from PySide6.QtGui import QCloseEvent

from Models.session_entity import SessionEntity


class SessionManager:
    def __init__(self):
        self.session_entity = SessionEntity()

    def set_session_id(self, session_id):
        self.session_entity.session_id = session_id

    def set_table_name(self, table_name):
        print(table_name)
        self.session_entity.table_name = table_name

    def set_table_rows(self, row_count):
        self.session_entity.table_row = row_count

    def set_table_cols(self, col_count):
        self.session_entity.table_col = col_count

    def set_table_headers(self, headers):
        self.session_entity.table_headers = headers

    def set_table_data(self, data):
        #print(data)
        #print("here")
        self.session_entity.table_data = data

    def write_to_settings(self):
        settings = QSettings()

        settings.beginGroup(self.session_entity.session_id)
        settings.beginGroup("encoding-table-panel")  # creates bin within session_id bin

        settings.setValue("title", self.session_entity.table_name)

        # need to leave the bin

        settings.endGroup()  # encoding-table-panel

        settings.beginGroup("encoding-table")  # creates encoding table bin

        # Save the row and column count.
        settings.setValue("rows", self.session_entity.table_row)
        settings.setValue("columns", self.session_entity.table_col)

        settings.beginWriteArray("headers", self.session_entity.table_col)
        for col_ix in range(self.session_entity.table_col):
            settings.setArrayIndex(col_ix)
            if self.session_entity.table_headers[col_ix] is not None:
                settings.setValue(
                    "header", self.session_entity.table_headers[col_ix])
            else:
                settings.setValue("header", str(col_ix + 1))
        settings.endArray()

        settings.beginGroup("table-data")  # creates table-data bin

        for rowIx in range(self.session_entity.table_row):
            settings.beginWriteArray(str(rowIx))
            for colIx in range(self.session_entity.table_col):
                settings.setArrayIndex(colIx)
                item = self.session_entity.table_data[rowIx][colIx]
                if item is not None and item != '':
                    settings.setValue("cell", item)
                    print(item)
                else:
                    settings.setValue("cell", None)
            settings.endArray()

        settings.endGroup()  # table-data
        settings.endGroup()  # encoding-table
        settings.endGroup()  # session-id

        print(self.session_entity.session_id)
        print(self.session_entity.table_col)
        print(self.session_entity.table_row)
        print(self.session_entity.table_name)
        print(self.session_entity.table_headers)

    def load_existing_session(self, session_id):

        self.session_entity.session_id = session_id
        settings = QSettings()

        settings.beginGroup(session_id)
        settings.beginGroup("encoding-table-panel")

        self.session_entity.table_name = settings.value("title")

        settings.endGroup()  # encoding-table-panel

        settings.beginGroup("encoding-table")

        # Update the row and column counts of the table.
        self.session_entity.table_row = (int(settings.value("rows")))
        self.session_entity.table_col = (int(settings.value("columns")))

        # Update the headers of the table.
        settings.beginReadArray("headers")
        for col_ix in range(self.session_entity.table_col):
            settings.setArrayIndex(col_ix)
            header = settings.value("header")
            self.session_entity.table_headers.append(header)
        settings.endArray()

        # Update the table data of the table.
        settings.beginGroup("table-data")
        for rowIx in range(self.session_entity.table_row):
            size = settings.beginReadArray(str(rowIx))
            for colIx in range(size):
                settings.setArrayIndex(colIx)
                cell_data = settings.value("cell")
                if cell_data is not None:
                    self.session_entity.table_data.append(cell_data, rowIx, colIx)
            settings.endArray()

        settings.endGroup()  # table-data
        settings.endGroup()  # encoding-table
        settings.endGroup()  # session-id

        print(self.session_entity.session_id)
        print(self.session_entity.table_col)
        print(self.session_entity.table_row)
        print(self.session_entity.table_name)
        print(self.session_entity.table_headers)
