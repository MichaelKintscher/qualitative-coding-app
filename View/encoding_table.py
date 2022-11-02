from PySide6 import QtWidgets
from PySide6.QtWidgets import QTableWidget


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
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.horizontalHeader().setDefaultSectionSize(60)
        self.horizontalHeader().setMaximumSectionSize(100)
        self.verticalHeader().setStretchLastSection(True)
        self.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.verticalHeader().setDefaultSectionSize(30)
        self.setStyleSheet("QTableWidget::item {border: 0px; padding: 5px;}")

        # Ensure at least 5 rows are visible at all times.
        self.minimum_visible_rows = 5
        total_border_height = 2
        self.setMinimumHeight(self.rowHeight(0) * (self.minimum_visible_rows + total_border_height))

    def add_column(self):
        """Increases the column count of the table by 1."""
        self.setColumnCount(self.columnCount() + 1)

    def add_row(self):
        """Increases the row count of the table by 1."""
        self.setRowCount(self.rowCount() + 1)