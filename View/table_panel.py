
from PySide6.QtWidgets import QWidget, QPushButton, QGridLayout, QSizePolicy, QComboBox, QLabel
from View.encoding_table import EncodingTable


class TablePanel(QWidget):
    """Container of all Encoding Table related widgets."""

    def __init__(self):
        """
        Constructor - Creates the related Encoding Table widgets and adds them
        to the panel using a QGridLayout.
        """
        super().__init__()

        self.table = EncodingTable()

        self.add_col_button = QPushButton("Add column")
        self.add_row_button = QPushButton("Add row")

        # Configure the add column button to expand vertically.
        self.add_col_button.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Expanding)

        """Creates font changing label and dropdown"""
        font_options = ["8", "9", "10", "11", "12", "14", "16",
                        "18", "20", "22", "24", "26", "28", "36", "48", "72"]
        self.change_font_label = QLabel("Change font: ")
        self.change_font_dropDown = QComboBox()
        self.change_font_dropDown.addItems(font_options)

        grid_layout = QGridLayout()
        grid_layout.addWidget(self.table, 0, 0)
        grid_layout.addWidget(self.add_col_button, 1, 1)
        grid_layout.addWidget(self.add_row_button, 1, 0)
        grid_layout.addWidget(self.change_font_label, 0, 1)
        grid_layout.addWidget(self.change_font_dropDown, 0, 2)

        self.setLayout(grid_layout)
