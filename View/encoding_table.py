from PySide6 import QtWidgets
from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem


class EncodingTable(QTableWidget):
    """
    EncodingTable is a custom QTableWidget used to support encoding table
    functionalities in the front-end.
    """

    def __init__(self):
        """
        Constructor - Sets the properties of a QTableWidget.
        """
        super().__init__()

        self.setRowCount(10)
        self.setColumnCount(4)

        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        self.horizontalHeader().setDefaultSectionSize(100)
        self.verticalHeader().setStretchLastSection(True)
        self.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.verticalHeader().setDefaultSectionSize(70)

        # Map the initial header values to [0, columnCount).
        for colIx in range(self.columnCount()):
            self.setHorizontalHeaderItem(colIx, QTableWidgetItem(str(colIx)))

        # Ensure at least 5 rows are visible at all times.
        self.minimum_visible_rows = 5
        total_border_height = 2
        self.setMinimumHeight(self.rowHeight(0) * (self.minimum_visible_rows + total_border_height))

    def add_column(self):
        """
        Increases the column count of the table by 1.
        """
        self.setColumnCount(self.columnCount() + 1)

    def add_row(self):
        """
        Increases the row count of the table by 1.
        """
        self.setRowCount(self.rowCount() + 1)

    def read_settings(self, session_id):
        """
        Reads table settings and updates the table content to the saved state
        for the group with the given session_id.
        """
        settings = QSettings()
        settings.beginGroup(session_id)
        settings.beginGroup("encoding-table")

        # Update the column count of the table.
        self.setColumnCount(int(settings.value("columns")))

        # Update the headers of the table.
        for colIx in range(self.columnCount()):
            self.setHorizontalHeaderItem(colIx, QTableWidgetItem(str(colIx)))

        # Update the table data of the table.
        settings.beginGroup("table-data")
        for rowIx in range(self.rowCount()):
            size = settings.beginReadArray(str(rowIx))
            for colIx in range(size):
                settings.setArrayIndex(colIx)
                cell_data = settings.value("cell")
                if cell_data is not None:
                    self.setItem(rowIx, colIx, QTableWidgetItem(cell_data))
            settings.endArray()

        settings.endGroup()  # table-data
        settings.endGroup()  # encoding-table
        settings.endGroup()  # session-id
        
    def set_cell_size(self, width, height):
        """
        Changes default cell width.
        """
        self.horizontalHeader().setMinimumSectionSize(width)
        self.verticalHeader().setMinimumSectionSize(height)

    def set_maximum_width(self, width):
        """
        Changes default cell height.
        """
        self.horizontalHeader().setMaximumSectionSize(width)

    def set_padding(self, padding):
        """
        Changes default padding.
        """
        self.setStyleSheet("QTableWidget::item { padding: " + padding + "px }")
        
    def write_settings(self, session_id):
        """
        Writes the table data to the QSettings object for persistence.
        """
        settings = QSettings()
        settings.beginGroup(session_id)
        settings.beginGroup("encoding-table")

        # Save the column count.
        settings.setValue("columns", self.columnCount())

        # Save the table headers.
        settings.beginWriteArray("headers", self.columnCount())
        for colIx in range(self.columnCount()):
            settings.setArrayIndex(colIx)
            settings.setValue("header", self.horizontalHeaderItem(colIx).text())
        settings.endArray()

        # Save the table data
        settings.beginGroup("table-data")
        for rowIx in range(self.rowCount()):
            settings.beginWriteArray(str(rowIx))
            for colIx in range(self.columnCount()):
                settings.setArrayIndex(colIx)
                item = self.item(rowIx, colIx)
                if item is not None and item.text() != '':
                    settings.setValue("cell", item.text())
                else:
                    settings.setValue("cell", None)
            settings.endArray()

        settings.endGroup()  # table-data
        settings.endGroup()  # encoding-table
        settings.endGroup()  # session-id
