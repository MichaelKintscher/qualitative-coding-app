from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QLineEdit


class SessionCreatorPage(QDialog):
    """ Page to create new sessions. """

    def __init__(self):
        """
        Constructs a page with the necessary components to initialize and
        create a new session.
        """
        super().__init__()

        # Creates a vertical layout for the page
        vertical_layout = QVBoxLayout()

        # Creates a title for the page
        title = QLabel("Create New Session")
        title.setStyleSheet("font-size: 28px; padding-top: 10px; padding: 10px 10px 0px 10px")

        # Create inputs for the session name.
        session_label = QLabel("Session Name (required)")
        session_label.setStyleSheet("padding-left: 15px; margin-top: 40px")
        self.session_input = QLineEdit()
        self.session_input.setFixedWidth(300)
        self.session_input.setStyleSheet("margin-left: 15px")

        # Create inputs for the encoding table name.
        table_label = QLabel("Encoding Table Title (optional)")
        table_label.setStyleSheet("padding-left: 15px; margin-top: 40px")
        self.table_input = QLineEdit()
        self.table_input.setFixedWidth(300)
        self.table_input.setStyleSheet("margin-left: 15px")

        # Create inputs for loading a video.

        # Create the "Ok" and "Back" standard buttons
        #   (Note: There is no standard "back" button, though we can overwrite
        #    the text of a cancel button).
        self.dialog_buttons = QDialogButtonBox()
        self.dialog_buttons.addButton(QDialogButtonBox.Cancel).setText("Back")
        self.dialog_buttons.addButton(QDialogButtonBox.Ok)

        # Add the components to the page layout.
        vertical_layout.addWidget(title)
        vertical_layout.addWidget(session_label)
        vertical_layout.addWidget(self.session_input)
        vertical_layout.addWidget(table_label)
        vertical_layout.addWidget(self.table_input)
        vertical_layout.addStretch()
        vertical_layout.addWidget(self.dialog_buttons)
        self.setLayout(vertical_layout)
