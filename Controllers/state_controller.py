from PySide6.QtCore import Slot


from Controllers.project_management_controller import ProjectManagementController
from Controllers.window_controller import WindowController

from View.main_window import MainWindow
from View.project_management_window import ProjectManagementWindow

from Application.session_manager import SessionManager
from Application.global_settings_manager import GlobalSettingsManager


class StateController:
    """
    The StateController manages and responds to program state changes.
    A program state represents whether the application is currently
    running, and responding to events dependent on program state.
    """

    def __init__(self):
        """
        Constructs an instance of the state controller, initializing
        the state appropriate for an unstarted project.
        """
        self.program_running = False
        self.project_management_window = ProjectManagementWindow()
        self.project_management_controller = ProjectManagementController(self.project_management_window, self)
        self.window = None
        self.window_controller = None
        self.session_manager = SessionManager()
        self.global_settings_manager = GlobalSettingsManager()

    def create_new_session(self, session_name, table_name="Default Title", video=None):
        """
        Creates a new window, assigning it a window controller.
        """
        if self.window:
            return

        self.window = MainWindow(session_name)
        self.window_controller = WindowController(self.window, self.global_settings_manager)
        self.window.show()

        # Connect to the closing signal to call the function that writes all the data to entity and QSettings.
        self.window.closing.connect(lambda: self.write_session_slot(session_name))

    def exec_start(self):
        """
        Starts the application, displaying the session management window.
        """
        if self.program_running:
            return

        self.project_management_window.show()

    def load_session(self, session_id):
        """
        Loads the session with the session id.
        """
        if not self.program_running:
            self.window = MainWindow(session_id)
            self.window_controller = WindowController(self.window, self.global_settings_manager)
            self.window.show()

            # Given this session id go through all data and put in session entity.
            self.session_manager.load_existing_session(session_id)
            self.global_settings_manager.load_global_settings()

            # Call setters to set the values in the view with the values from our session entity.
            self.window.table_panel.set_table_name(self.session_manager.session_entity.table_name)
            self.window.table_panel.table.set_col_count(self.session_manager.session_entity.table_col_count)
            self.window.table_panel.table.set_row_count(self.session_manager.session_entity.table_row_count)
            self.window.table_panel.table.set_headers(self.session_manager.session_entity.table_headers)
            self.window.table_panel.table.set_table_data(self.session_manager.session_entity.table_data)

            # Connect to the closing signal to call the function that writes all the data to entity and QSettings.
            self.window.closing.connect(lambda: self.write_session_slot(session_id))

    @Slot()
    def write_session_slot(self, session_id):
        """
        Function that get data from the view and sends to manager.
        """
        self.session_manager.set_session_id(session_id)

        table_title = self.window.table_panel.get_table_name()
        self.session_manager.set_table_name(table_title)

        table_rows = self.window.table_panel.table.get_row_count()
        self.session_manager.set_table_row_count(table_rows)

        table_cols = self.window.table_panel.table.get_col_count()
        self.session_manager.set_table_col_count(table_cols)

        table_headers = self.window.table_panel.table.get_headers()
        self.session_manager.set_table_headers(table_headers)

        table_data = self.window.table_panel.table.get_table_data()
        self.session_manager.set_table_data(table_data)

        # Call function to write everything to QSettings.
        self.session_manager.write_to_settings()
