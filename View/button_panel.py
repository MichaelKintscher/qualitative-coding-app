from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout


class ButtonPanel(QWidget):
    """Container of all Coding Assistance buttons."""

    def __init__(self):
        """
        Constructor - Creates the Coding Assistance buttons and adds them
        into a QHBoxLayout.
        """
        super().__init__()

        # Create four placeholder buttons
        button1 = QPushButton("Button 1")
        button2 = QPushButton("Button 2")
        button3 = QPushButton("Button 3")
        button4 = QPushButton("Button 4")

        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(button1, stretch=1)
        horizontal_layout.addWidget(button2, stretch=1)
        horizontal_layout.addWidget(button3, stretch=1)
        horizontal_layout.addWidget(button4, stretch=1)
        self.setLayout(horizontal_layout)
