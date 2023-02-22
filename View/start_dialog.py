from PySide6.QtCore import Slot, QSettings
from PySide6.QtWidgets import QDialog, QVBoxLayout, QButtonGroup, QDialogButtonBox, QPushButton


class StartDialog(QDialog):
    """
    Dialog window that greets the user before the main application window is
    opened. The user can choose, using the dialog options, whether they want
    to open a new session of the application or load a previous session. The
    previous sessions are read using the global QSettings object. Once the
    decision is made, the session id is saved and can be accessed from
    the initiator of the dialog box.
    """
    def __init__(self):
        """Construct the startup dialog and its internal components."""
        super().__init__()

        self.setWindowTitle("Welcome to the Qualitative Coding Desktop App")

        # Attribute that will remember the chosen session ID
        self.session_id = None

        # Create the "Ok" and "Cancel" standard buttons and set up their slot functions.
        dialog_buttons = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        dialog_buttons.button(QDialogButtonBox.Ok).clicked.connect(self.slot_ok)
        dialog_buttons.button(QDialogButtonBox.Cancel).clicked.connect(self.slot_cancel)

        # Create a container for the buttons of the layout
        self.button_container = QButtonGroup()

        # Create a button for the "New Session" option.
        new_session_button = QPushButton("New Session")
        self.button_container.addButton(new_session_button)

        # Add buttons for the saved sessions
        self.load_and_add_session_buttons()

        # Iterate through all the buttons in the container and make them
        # act like radio buttons.
        for button in self.button_container.buttons():
            button.setCheckable(True)
            button.setAutoExclusive(True)

        # Set the layout of the dialog box to a vertical layout and add
        # all the widgets to it.
        vertical_layout = QVBoxLayout()
        for button in self.button_container.buttons():
            vertical_layout.addWidget(button)
        vertical_layout.addWidget(dialog_buttons)
        self.setLayout(vertical_layout)

    def load_and_add_session_buttons(self):
        """
        Reads through the QSettings groups and adds a button for each group
        name (session ID).
        """
        settings = QSettings()
        for group in settings.childGroups():
            button = QPushButton(group)
            self.button_container.addButton(button)

    @Slot()
    def slot_ok(self):
        """
        Slot function for the "OK" button. This event handler gets the selected
        session button and returns its value as a result. If no button is
        selected, then this function does nothing.
        """
        if self.button_container.checkedButton() is None:
            return

        self.session_id = self.button_container.checkedButton().text()
        self.accept()

    @Slot()
    def slot_cancel(self):
        """
        If the user cancels the QDialogButtonBox, then reject the entire dialog
        box.
        """
        self.reject()
