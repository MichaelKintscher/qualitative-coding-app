from PySide6.QtCore import QSettings

from Models.session_entity import SessionEntity


class SessionManager:
    """
    SessionManager is a manager for the current session that takes acts
    as a middleman setting and getting data between the session entity
    and QSettings to send back to the state controller.
    """

    def __init__(self):
        """
        Constructor - constructs an instance of our session entity
        """
        self.session_entity = SessionEntity()

    def set_table_name(self, table_name):
        """
        Sets the session entity table name.

        Parameters:
            table name
        """
        self.session_entity.table_name = table_name

    def set_table_row_count(self, row_count):
        """
        Sets the session entity row count

        Parameters:
            table row count
        """
        self.session_entity.table_row_count = row_count

    def set_table_col_count(self, col_count):
        """
        Sets the session entity column count

        Parameters:
            table column count
        """
        self.session_entity.table_col_count = col_count

    def set_table_headers(self, headers):
        """
        Sets the session entity table headers

        Parameters:
            table header list
        """
        self.session_entity.table_headers = headers

    def set_table_data(self, data):
        """
        Sets the session entity table data

        Parameters:
            table data 2D list
        """
        self.session_entity.table_data = data

    def set_session_id(self, session_id):
        """
        Sets the session entity session id.

        Parameters:
            session id
        """
        self.session_entity.session_id = session_id

    def write_to_settings(self):
        """
        Takes the data in our session entity and writes it to QSettings
        saved under a key of the session id name.
        """
        settings = QSettings()
        settings.beginGroup("sessions")

        settings.beginGroup(self.session_entity.session_id)
        settings.beginGroup("encoding-table-panel")  # creates bin within session_id bin

        settings.setValue("title", self.session_entity.table_name)

        settings.endGroup()  # need to leave encoding-table-panel bin

        settings.beginGroup("encoding-table")  # creates encoding table bin

        # Save the row and column count.
        settings.setValue("rows", self.session_entity.table_row_count)
        settings.setValue("columns", self.session_entity.table_col_count)

        settings.beginWriteArray("headers", self.session_entity.table_col_count)
        for col_ix in range(self.session_entity.table_col_count):
            settings.setArrayIndex(col_ix)
            if self.session_entity.table_headers[col_ix] is not None:
                settings.setValue(
                    "header", self.session_entity.table_headers[col_ix])
            else:
                settings.setValue("header", str(col_ix + 1))
        settings.endArray()

        settings.beginGroup("table-data")  # creates table-data bin

        for rowIx in range(self.session_entity.table_row_count):
            settings.beginWriteArray(str(rowIx))
            for colIx in range(self.session_entity.table_col_count):
                settings.setArrayIndex(colIx)
                item = self.session_entity.table_data[rowIx][colIx]
                if item is not None and item != '':
                    settings.setValue("cell", item)
                else:
                    settings.setValue("cell", None)
            settings.endArray()

        settings.endGroup()  # sessions
        settings.endGroup()  # table-data
        settings.endGroup()  # encoding-table
        settings.endGroup()  # session-id

    def load_existing_session(self, session_id):
        """
        Takes a session id and looks in QSettings to gather the data
        from there and load our session entity.

        Parameters:
            session id name
        """
        self.session_entity.session_id = session_id
        settings = QSettings()
        settings.beginGroup("sessions")

        settings.beginGroup(session_id)
        settings.beginGroup("encoding-table-panel")

        self.session_entity.table_name = settings.value("title")

        settings.endGroup()  # encoding-table-panel

        settings.beginGroup("encoding-table")

        # Update the row and column counts of the table.
        self.session_entity.table_row_count = (int(settings.value("rows")))
        self.session_entity.table_col_count = (int(settings.value("columns")))

        # Update the headers of the table.
        settings.beginReadArray("headers")
        for col_ix in range(self.session_entity.table_col_count):
            settings.setArrayIndex(col_ix)
            header = settings.value("header")
            self.session_entity.table_headers.append(header)
        settings.endArray()

        # Update the table data of the table.
        row_data = []
        settings.beginGroup("table-data")
        for rowIx in range(self.session_entity.table_row_count):
            size = settings.beginReadArray(str(rowIx))
            col_data = []
            for colIx in range(size):
                settings.setArrayIndex(colIx)
                cell_data = settings.value("cell")
                if cell_data is not None:
                    col_data.append(cell_data)
                else:
                    col_data.append(None)
            row_data.append(col_data)
            settings.endArray()
        self.session_entity.table_data = row_data

        settings.endGroup()  # sessions
        settings.endGroup()  # table-data
        settings.endGroup()  # encoding-table
        settings.endGroup()  # session-id
