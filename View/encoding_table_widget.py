import sys
from PySide6 import QtWidgets, QtCore, QtGui


class EncodingTableWidget(QtWidgets.QWidget):
    def __init__(self):
        """
        Constructor - Initializes a QTableWidget and an Add Row button in a vertical layout.
        """
        super().__init__()

        self._table = QtWidgets.QTableWidget()
        self._table.setRowCount(10)
        self._table.setColumnCount(4)

        self._table.horizontalHeader().setStretchLastSection(True)
        self._table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self._table.verticalHeader().setStretchLastSection(True)
        self._table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self._add_row_button = QtWidgets.QPushButton("Add Row")
        self._add_row_button.setGeometry(QtCore.QRect(200, 150, 93, 28))

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.addWidget(self._add_row_button)
        self._layout.addWidget(self._table)
        self.setLayout(self._layout)

    def add_row(self):
        """Increases the row count of the table by 1."""
        self._table.setRowCount(self._table.rowCount() + 1)

    def connect_add_table_row_to_slot(self, slot):
        """Connects the add row button to the provided slot function."""
        self._add_row_button.clicked.connect(slot)
