from PySide6.QtCore import QSettings, Slot
from PySide6.QtWidgets import QDialogButtonBox

from View.session_option import SessionOption


class ProjectManagementController:
    """
    The ProjectManagementController manages and responds to input events
    from the project management window.
    """

    def __init__(self, project_management_window, state_controller):
        """ Construct an instance of the project management controller. """
        self.project_management_window = project_management_window
        self.state_controller = state_controller

        # Get access to the pages of the project management window.
        self.session_manager_page = self.project_management_window.get_widget(0)
        self.session_creator_page = self.project_management_window.get_widget(1)

        # Connect slot functions to the appropriate signals in the pages.
        self.session_manager_page.create_session_button.clicked.connect(self.switch_to_session_creation_page)
        self.session_manager_page.clear_sessions_button.clicked.connect(self.clear_sessions)

        self.session_creator_page.dialog_buttons.button(QDialogButtonBox.Cancel).clicked.connect(self.back_to_mgmt_page)
        self.session_creator_page.dialog_buttons.button(QDialogButtonBox.Ok).clicked.connect(self.create_session)

        self.session_manager_page.user_settings_button.clicked.connect(self._open_settings_dialog)

        # Iterate through all SessionOptions in the session list in the
        #   Session Manager Page and connect their signals
        session_list_layout = self.session_manager_page.session_list.layout()
        for i in range(session_list_layout.count()):
            session_item = session_list_layout.itemAt(i)
            if session_item and session_item.widget():
                session_option = session_item.widget()
                session_name = session_option.session_button.text()
                session_option.session_button.clicked.connect(self.make_lambda(self.load_session, session_name))
                session_option.remove_session_button.clicked.connect(self.make_lambda(self.delete_session, session_option))

    @Slot()
    def back_to_mgmt_page(self):
        """
        Switches the current page of the project management page to the
        management page.
        """
        self.project_management_window.set_current_widget(0)

    @Slot()
    def clear_sessions(self):
        """ Clears all saved sessions. """
        settings = QSettings()
        settings.remove("sessions")

        # Delete sessions from graphical session list.
        session_list_layout = self.session_manager_page.session_list.layout()
        while session_list_layout.count():
            child = session_list_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def create_session(self):
        """
        Attempts to create a new session with the user-input fields
        of the session creator page.
        """
        session_name = self.session_creator_page.session_input.text()
        if session_name == "" or not self.is_unique_session_name(session_name):
            return

        self.state_controller.create_new_window(session_name)
        self.session_creator_page.parent().close()

    @Slot(SessionOption)
    def delete_session(self, session_option):
        """
        Deletes the session_option from the session_list at index i,
        removing it from the QSettings object and the session list.
        """
        session_list = self.session_manager_page.session_list.layout()
        session_name = session_option.session_button.text()

        # Remove the session from storage.
        settings = QSettings()
        settings.beginGroup("sessions")
        settings.remove(session_name)
        settings.endGroup()

        # Remove the session from the session list
        child = session_list.takeAt(session_list.indexOf(session_option))
        if child.widget():
            child.widget().deleteLater()

    @staticmethod
    def is_unique_session_name(session_name):
        """
        Determines whether the session_id has been previously stored (case-insensitive).

        Return:
            True if the session_id has been previously stored, False otherwise.
        """
        settings = QSettings()
        settings.beginGroup("sessions")
        session_name = session_name.lower()
        for session in settings.childGroups():
            if session.lower() == session_name:
                return False
        return True

    @Slot(str)
    def load_session(self, session_id):
        """
        Loads the session with the given session_id name.

        Parameters:
            session_id: identifier of session to load.
        """
        self.state_controller.load_session(session_id)
        self.session_manager_page.parent().close()

    @staticmethod
    def make_lambda(func, param):
        """
        Helper function that creates a new instance of a lambda function.
        """
        return lambda: func(param)

    @Slot()
    def switch_to_session_creation_page(self):
        """
        Switches the current page in the project management window to the
        session creation page.
        """
        self.project_management_window.set_current_widget(1)

    @Slot()
    def _open_settings_dialog(self):
        """
        Opens the settings dialog.
        """
        self.state_controller.user_settings_controller.open_settings_dialog()
