import sys

from PySide6 import QtWidgets
from PySide6.QtCore import QRect
from PySide6.QtWidgets import QWidget, QTableWidget, QPushButton, QVBoxLayout


class EncodingTableWidget(QWidget):
    def __init__(self):
        """
        Constructor - Initializes a QTableWidget and an Add Row button in a vertical layout.
        """
        super().__init__()

        self._table = QTableWidget()
        self._table.setRowCount(10)
        self._table.setColumnCount(4)

        self._table.horizontalHeader().setStretchLastSection(True)
        self._table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self._table.verticalHeader().setStretchLastSection(True)
        self._table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self._add_row_button = QPushButton("Add Row")
        self._add_col_button = QPushButton("Add column")
        self._add_row_button.setGeometry(QRect(200, 150, 93, 28))
        self._add_col_button.setGeometry(QRect(200, 150, 93, 28))

        self._layout = QVBoxLayout()
        self._layout.addWidget(self._add_row_button)
        self._layout.addWidget(self._add_col_button)
        self._layout.addWidget(self._table)
        self.setLayout(self._layout)

    def add_column(self):
        """Increases the column count of the table by 1."""
        self._table.setColumnCount(self._table.columnCount() + 1)

    def add_row(self):
        """Increases the row count of the table by 1."""
        self._table.setRowCount(self._table.rowCount() + 1)

    def connect_add_table_col_to_slot(self, slot):
        """Connects the add column button to the provided slot function."""
        self._add_col_button.clicked.connect(slot)

    def connect_add_table_row_to_slot(self, slot):
        """Connects the add row button to the provided slot function."""
        self._add_row_button.clicked.connect(slot)
