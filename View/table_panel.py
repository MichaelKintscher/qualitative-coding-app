from PySide6 import QtCore
from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QWidget, QPushButton, QGridLayout, QSizePolicy, QComboBox, QLabel, QLineEdit
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

        self.title = QLineEdit(self)
        self.title.setText("Table Title")
        self.title.setAlignment(QtCore.Qt.AlignCenter)

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
        grid_layout.addWidget(self.title, 0, 0, QtCore.Qt.AlignCenter)
        grid_layout.addWidget(self.table, 1, 0)
        grid_layout.addWidget(self.add_col_button, 2, 1)
        grid_layout.addWidget(self.add_row_button, 2, 0)
        grid_layout.addWidget(self.change_font_label, 1, 1)
        grid_layout.addWidget(self.change_font_dropDown, 1, 2)

        self.setLayout(grid_layout)

    def read_settings(self, session_id):
        """
        Reads table panel settings and updates the table panel content to the saved state
        for the group with the given session_id.
        """
        settings = QSettings()
        settings.beginGroup(session_id)
        settings.beginGroup("encoding-table-panel")

        self.title.setText(settings.value("title"))

        settings.endGroup()  # encoding-table-panel
        settings.endGroup()  # session-id

    def write_settings(self, session_id):
        """
        Writes the table panel data to the QSettings object for persistence.
        """
        settings = QSettings()
        settings.beginGroup(session_id)
        settings.beginGroup("encoding-table-panel")

        settings.setValue("title", self.title.text())

        settings.endGroup()  # encoding-table-panel
        settings.endGroup()  # session-id
