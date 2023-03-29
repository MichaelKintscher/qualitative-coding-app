from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QPushButton, QGridLayout, QSizePolicy, QComboBox, QLabel, QLineEdit
from View.encoding_table import EncodingTable
from PySide6.QtCore import Qt


class TablePanel(QWidget):
    """Container of all Encoding Table related widgets."""

    def __init__(self):
        """
        Constructor - Creates the related Encoding Table widgets and adds them
        to the panel using a QGridLayout.
        """
        super().__init__()

        self.table = EncodingTable()

        self.title = QLineEdit(self)
        self.title.setText("Table Title")
        self.title.setAlignment(QtCore.Qt.AlignCenter)

        self.add_col_button = QPushButton("Add column")
        self.add_row_button = QPushButton("Add row")
        self.delete_col_button = QPushButton("Delete current column")
        self.delete_row_button = QPushButton("Delete current row")

        # Configure the add column button to expand vertically.
        self.add_col_button.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Expanding)

        """Creates font changing label and dropdown"""
        """font_options = ["8", "9", "10", "11", "12", "14", "16",
                        "18", "20", "22", "24", "26", "28", "36", "48", "72"]
        self.change_font_label = QLabel("Change font: ")
        self.change_font_dropDown = QComboBox()
        self.change_font_dropDown.addItems(font_options)"""

        grid_layout = QGridLayout()
        grid_layout.addWidget(self.title, 0, 0, QtCore.Qt.AlignCenter)
        grid_layout.addWidget(self.table, 1, 0)
        grid_layout.addWidget(self.add_col_button, 1, 1, alignment=Qt.AlignCenter)
        grid_layout.addWidget(self.add_row_button, 1, 1, alignment=Qt.AlignBottom)
        #grid_layout.addWidget(self.change_font_label, 1, 1, alignment=Qt.AlignTop)
        #grid_layout.addWidget(self.change_font_dropDown, 1, 2, alignment=Qt.AlignTop|Qt.AlignLeft)
        grid_layout.addWidget(self.delete_col_button, 1, 2, alignment=Qt.AlignCenter)
        grid_layout.addWidget(self.delete_row_button, 1, 2, alignment=Qt.AlignBottom)
        self.setLayout(grid_layout)

    def get_table_name(self):
        """
        Getter to get the table name.

        Returns:
            A string of the table name
        """
        return self.title.text()

    def set_table_name(self, table_name):
        """
        Sets the table name of the view.

        Parameters:
            A string of the table name
        """
        self.title.setText(table_name)
