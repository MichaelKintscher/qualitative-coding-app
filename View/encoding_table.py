from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QLineEdit
from PySide6 import QtWidgets, QtCore


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
        self.verticalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeToContents)
        self.verticalHeader().setDefaultSectionSize(70)

        # Map the initial header values to [1, columnCount].
        for col_ix in range(self.columnCount()):
            self.setHorizontalHeaderItem(col_ix, QTableWidgetItem(str(col_ix + 1)))

        # Ensure at least 5 rows are visible at all times.
        self.minimum_visible_rows = 5
        total_border_height = 2
        self.setMinimumHeight(self.rowHeight(
            0) * (self.minimum_visible_rows + total_border_height))

        """Sets up QLineEdit item over headers"""
        self.horizontalHeader().line = QLineEdit(
            parent=self.horizontalHeader().viewport())
        self.horizontalHeader().line.setAlignment(QtCore.Qt.AlignTop)
        self.horizontalHeader().line.setHidden(True)
        self.horizontalHeader().line.blockSignals(True)
        self.horizontalHeader().sectionedit = 0

        """Makes columns take up even space. It's not perfect but width/4 doesn't work either"""
        for column in range(self.columnCount()):
            self.setColumnWidth(column, self.width()/2)

        """Sets the first column header to 'Time'"""
        self.setHorizontalHeaderLabels(["Time"])

        """Creates a QTableWidgetItem for all column headers whose type is None"""
        for column in range(self.columnCount()):
            if self.horizontalHeaderItem(column) is None:
                self.setHorizontalHeaderItem(
                    column, QTableWidgetItem(str(column)))

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

    def change_font(self, font_choice):
        """
        Changes font size of cells.

        Parameters:
            font_choice: size of user selected font.
        """
        font = self.font()
        font.setPointSize(font_choice)
        self.setFont(font)

    def edit_header(self, section):
        """
        Enables the QLineEdit item over headers to be editable.

        Parameters:
            section: keeps track of which column header is being edited.
        """
        if section != 0:
            edit_geo = self.horizontalHeader().line.geometry()
            edit_geo.setWidth(self.horizontalHeader().sectionSize(section))
            edit_geo.moveLeft(
                self.horizontalHeader().sectionViewportPosition(section))
            self.horizontalHeader().line.setGeometry(edit_geo)

            self.horizontalHeader().line.setHidden(False)
            self.horizontalHeader().line.blockSignals(False)
            self.horizontalHeader().line.setFocus()
            self.horizontalHeader().line.selectAll()
            self.horizontalHeader().sectionedit = section

    def done_editing(self):
        """Updates header text when user is done editing QLineEdit item."""
        self.horizontalHeader().line.blockSignals(True)
        self.horizontalHeader().line.setHidden(True)
        new_label = str(self.horizontalHeader().line.text())

        if new_label != '':
            self.setHorizontalHeaderItem(
                self.horizontalHeader().sectionedit, QTableWidgetItem(new_label))
            self.horizontalHeader().line.setText('')
            self.horizontalHeader().setCurrentIndex(QtCore.QModelIndex())

    def read_settings(self, session_id):
        """
        Reads table settings and updates the table content to the saved state
        for the group with the given session_id.
        """
        settings = QSettings()
        settings.beginGroup(session_id)
        settings.beginGroup("encoding-table")

        # Update the row and column counts of the table.
        self.setRowCount(int(settings.value("rows")))
        self.setColumnCount(int(settings.value("columns")))

        # Update the headers of the table.
        settings.beginReadArray("headers")
        for col_ix in range(self.columnCount()):
            settings.setArrayIndex(col_ix)
            header = settings.value("header")
            self.setHorizontalHeaderItem(col_ix, QTableWidgetItem(header))
        settings.endArray()

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

        # Save the row and column count.
        settings.setValue("rows", self.rowCount())
        settings.setValue("columns", self.columnCount())

        # Save the table headers.
        settings.beginWriteArray("headers", self.columnCount())
        for col_ix in range(self.columnCount()):
            settings.setArrayIndex(col_ix)
            if self.horizontalHeaderItem(col_ix) is not None:
                settings.setValue(
                    "header", self.horizontalHeaderItem(col_ix).text())
            else:
                settings.setValue("header", str(col_ix + 1))
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
