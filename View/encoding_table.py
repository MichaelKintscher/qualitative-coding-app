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

        # Sets up QLineEdit item over headers.
        self.horizontalHeader().line = QLineEdit(
            parent=self.horizontalHeader().viewport())
        self.horizontalHeader().line.setAlignment(QtCore.Qt.AlignTop)
        self.horizontalHeader().line.setHidden(True)
        self.horizontalHeader().line.blockSignals(True)
        self.horizontalHeader().sectionedit = 0

        # Makes columns take up even space. It's not perfect but width/4 doesn't work either.
        for column in range(self.columnCount()):
            self.setColumnWidth(column, self.width()/2)

        # Sets the first column header to 'Time'.
        self.setHorizontalHeaderLabels(["Time"])

        # Creates a QTableWidgetItem for all column headers whose type is None.
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

    def del_column(self):
        """
        Deletes current selected column
        """
        if self.columnCount() > 1:
            current_col = self.currentColumn()
            item_list = self.selectedIndexes()
            if current_col != 0 and len(item_list) > 0:
                self.removeColumn(current_col)

    def del_row(self):
        """
        Deletes current selected row
        """

        if self.rowCount() > 1:
            current_row = self.currentRow()
            item_list = self.selectedIndexes()
            num_columns = self.columnCount()
            num_rows = self.rowCount()
            row = False
            col = False

            # This logic determines whether a column or a row is selected
            if num_columns == 1:
                if len(item_list) == 0:
                    return
                elif len(item_list) == num_rows:
                    col = True
                else:
                    row = True
            elif len(item_list) > 1:
                row1 = item_list[0].row()
                col1 = item_list[0].column()
                row2 = item_list[1].row()
                col2 = item_list[1].column()

                if row1 == row2 and col1 != col2:
                    row = True
                if row1 != row2 and col1 == col2:
                    col = True

            if current_row == -1 or col:
                return
            elif row:
                self.removeRow(current_row)

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

    def get_row_count(self):
        """
        Getter method to get the row count.

        Returns:
            Int that is row count
        """
        return self.rowCount()

    def get_col_count(self):
        """
        Getter method to get the column count.

        Returns:
            Int that is column count
        """
        return self.columnCount()

    def get_headers(self):
        """
        Getter method to get table headers.

        Returns:
            List of headers
        """
        table_headers = []
        for col_ix in range(self.columnCount()):
            if self.horizontalHeaderItem(col_ix) is not None:
                table_headers.append(self.horizontalHeaderItem(col_ix).text())
            else:
                table_headers.append(str(col_ix + 1))
        return table_headers

    def get_table_data(self):
        """
        Getter method to get the table data.

        Returns:
            2D list of table data
        """
        row_data = []
        for row_ix in range(self.rowCount()):
            col_data = []
            for col_ix in range(self.columnCount()):
                item = self.item(row_ix, col_ix)
                if item is not None and item.text() != '':
                    col_data.append(item.text())
                else:
                    col_data.append(None)
            row_data.append(col_data)
        return row_data

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

    def set_row_count(self, table_row):
        """
        Sets the row count of the view.

        Parameter:
            int of table rows
        """
        self.setRowCount(table_row)

    def set_col_count(self, table_col):
        """
        Sets the column count of the view.

        Parameter:
            int of table columns
        """
        self.setColumnCount(table_col)

    def set_headers(self, table_headers):
        """
        Sets the table headers of the view.

        Parameters:
            list of table headers
        """
        for col_ix in range(self.columnCount()):
            header = table_headers[col_ix]
            self.setHorizontalHeaderItem(col_ix, QTableWidgetItem(header))

    def set_table_data(self, table_data):
        """
        Sets the table data of the view.

        Parameters:
            2D list of table data
        """
        for row_ix in range(self.rowCount()):
            for col_ix in range(self.columnCount()):
                cell_data = table_data[row_ix][col_ix]
                if cell_data is not None:
                    self.setItem(row_ix, col_ix, QTableWidgetItem(table_data[row_ix][col_ix]))
