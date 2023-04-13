from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QWidget, QScrollArea, QPushButton, QGridLayout, \
    QHBoxLayout, QSizePolicy, QStyle, QMenuBar

from View.session_option import SessionOption


class SessionManagerPage(QDialog):
    """ Page to manage recent sessions or create new sessions. """

    def __init__(self):
        """
        Constructs the dialog page with the necessary components to manage
        sessions.
        """
        super().__init__()

        # Layout to encapsulate all components of session manager page.
        grid_layout = QGridLayout()

        # Create a page title
        title = QLabel("Qualitative Coding Desktop Application")
        title.setStyleSheet("font-size: 28px; padding-top: 10px; padding: 10px 10px 0px 10px")

        # Component/Layout to encapsulate "recent sessions"
        recent_component = QWidget()
        recent_vertical_layout = QVBoxLayout()

        # Create a horizontal layout to encapsulate the recent title and a clear all button.
        recent_title_horizontal_layout = QHBoxLayout()
        recent_title = QWidget()

        # Create a label for the "recent" section
        recent_label = QLabel("Open Recent")
        recent_label.setStyleSheet("font-size: 16px;")

        # Create a clear all session button
        self.clear_sessions_button = QPushButton("Clear all sessions")
        self.clear_sessions_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Create a user settings button
        self.user_settings_button = QPushButton("User Settings")
        self.user_settings_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Add recent title and push button to horizontal layout
        recent_title_horizontal_layout.addWidget(recent_label)
        recent_title_horizontal_layout.addStretch()
        recent_title_horizontal_layout.addWidget(self.clear_sessions_button)
        recent_title_horizontal_layout.addWidget(self.user_settings_button)
        recent_title.setLayout(recent_title_horizontal_layout)

        # Scrollable viewport for list of sessions
        scroll_area = QScrollArea()
        self.session_list = self.create_session_list()
        scroll_area.setWidget(self.session_list)

        # Add the recent widgets to its widget component
        recent_vertical_layout.addWidget(recent_title)
        recent_vertical_layout.addWidget(scroll_area)
        recent_vertical_layout.addStretch()
        recent_component.setLayout(recent_vertical_layout)

        # Component/Layout to encapsulate "getting started"
        start_component = QWidget()
        start_vertical_layout = QVBoxLayout()

        # Create a label for the "starting" section
        self.start_label = QLabel("Getting Started")
        self.start_label.setStyleSheet("font-size: 16px; padding-right: 10px; padding-bottom: 10px")

        # Button to create a new session
        self.create_session_button = QPushButton("Create New Session")

        # Add "getting started" widgets to its widget component
        start_vertical_layout.addWidget(self.start_label)
        start_vertical_layout.addWidget(self.create_session_button)
        start_vertical_layout.addStretch()
        start_component.setLayout(start_vertical_layout)

        # Add page components to the encapsulating layout
        grid_layout.addWidget(title, 0, 0)
        grid_layout.addWidget(recent_component, 1, 0)
        grid_layout.addWidget(start_component, 1, 2)
        self.setLayout(grid_layout)

    @staticmethod
    def create_session_list():
        """
        Creates a widget containing a vertical layout of previously loaded
        sessions with buttons for deletion.
        """
        container_widget = QWidget()
        vertical_layout = QVBoxLayout()

        # Get access to stored session data
        settings = QSettings()
        settings.beginGroup("sessions")
        for session_id in settings.childGroups():
            session_option = SessionOption(session_id)
            vertical_layout.addWidget(session_option)
        settings.endGroup()

        vertical_layout.addStretch()
        container_widget.setLayout(vertical_layout)
        return container_widget

    def hide_session_creation_elements(self):
        """
        Hides the session creation related elements from the window. This method
        may be useful if we want to only want to display the session manager page.
        """
        self.create_session_button.hide()
        self.start_label.hide()

    def hide_user_setting_element(self):
        """
        Hides the user setting button element from the window. This method
        may be useful if we want to only want to display the session manager page.
        """
        self.user_settings_button.hide()

