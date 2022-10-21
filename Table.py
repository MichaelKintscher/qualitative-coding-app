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

        self._addRowButton = QtWidgets.QPushButton("Add Row")
        self._addRowButton.setGeometry(QtCore.QRect(200,150,93,28))
        self._addRowButton.clicked.connect(addrow())

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.addWidget(self.addRowButton)
        self._layout.addWidget(self.table)
        self.setLayout(self.layout)
