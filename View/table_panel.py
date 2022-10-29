from PySide6.QtWidgets import QWidget, QPushButton, QGridLayout, QSizePolicy

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

        grid_layout = QGridLayout()
        grid_layout.addWidget(self.table, 0, 0)
        grid_layout.addWidget(self.add_col_button, 0, 1)
        grid_layout.addWidget(self.add_row_button, 1, 0)
        self.setLayout(grid_layout)
