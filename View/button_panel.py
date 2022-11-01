from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QSizePolicy, QGridLayout


class ButtonPanel(QWidget):
    """Container of all Coding Assistance buttons."""

    def __init__(self):
        """
        Constructor - Creates the Coding Assistance buttons and adds them
        into a QHBoxLayout.
        """
        super().__init__()

        button_container = QWidget()
        horizontal_layout = QHBoxLayout()

        # Create four placeholder buttons.
        buttons = [QPushButton("Button 1"), QPushButton("Button 2"),
                   QPushButton("Button 3"), QPushButton("Button 4")]

        # Add each button to the horizontal layout and set their sizing policies.
        for button in buttons:
            horizontal_layout.addWidget(button, stretch=1)
            button.setSizePolicy(
                QSizePolicy.Preferred,
                QSizePolicy.Expanding)

        button_container.setLayout(horizontal_layout)

        # Add css styling to the container to give it a background color.
        button_container.setProperty("class", "button-container")
        self.setStyleSheet('''
            .button-container {
                background-color: #c5cbd4;
                border: 1px solid black;
                border-radius: 5%;
            }
        ''')

        # Add the button container to the button panel.
        self.setLayout(QGridLayout())
        self.layout().addWidget(button_container)
