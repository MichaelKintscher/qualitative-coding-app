from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QLineEdit
from PySide6.QtGui import QFont


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
        self.horizontalHeader().setDefaultSectionSize(60)
        self.horizontalHeader().setMaximumSectionSize(400)
        self.verticalHeader().setStretchLastSection(True)
        self.verticalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeToContents)
        self.verticalHeader().setDefaultSectionSize(30)
        self.setStyleSheet("QTableWidget::item {border: 0px; padding: 5px;}")

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

        """Ensure at least 5 rows are visible at all times."""
        self.minimum_visible_rows = 5
        total_border_height = 2
        self.setMinimumHeight(self.rowHeight(
            0) * (self.minimum_visible_rows + total_border_height))

        """Sets the first column header to 'Time'"""
        self.setHorizontalHeaderLabels(["Time"])

        """Creates a QTableWidgetItem for all column headers whose type is None"""
        for column in range(self.columnCount()):
            if self.horizontalHeaderItem(column) is None:
                self.setHorizontalHeaderItem(
                    column, QTableWidgetItem(str(column)))

    def add_column(self):
        """Increases the column count of the table by 1."""
        self.setColumnCount(self.columnCount() + 1)

        """Creates QTableWidgetItem for new column"""
        column = self.columnCount() - 1
        self.setHorizontalHeaderItem(column, QTableWidgetItem(str(column)))

    def add_row(self):
        """Increases the row count of the table by 1."""
        self.setRowCount(self.rowCount() + 1)

    def change_font(self, font_choice):
        """
        Changes font size of cells.

        Parameters:
            font_choice: size of user selected font
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
