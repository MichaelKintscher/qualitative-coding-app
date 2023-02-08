from PySide6.QtCore import Slot
from PySide6.QtGui import QCloseEvent

from Controllers.project_management_controller import ProjectManagementController
from Controllers.window_controller import WindowController
from View.main_window import MainWindow
from View.project_management_window import ProjectManagementWindow
from Application.session_manager import SessionManager


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

    def create_new_session(self, session_name, table_name="Default Title", video=None):
        """
        Creates a new window, assigning it a window controller.
        """
        if self.window:
            return

        self.window = MainWindow(session_name)
        self.window_controller = WindowController(self.window)
        self.window.show()
        self.window.closing.connect(self.write_session_slot(session_name))

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
            self.window_controller = WindowController(self.window)
            self.window.show()
            # given this session id go thru all data and put in session entity
            self.session_manager.load_existing_session(session_id)

            # call setters
            self.window.table_panel.set_table_name(self.session_manager.session_entity.table_name)
            self.window.table_panel.table.set_col_count(self.session_manager.session_entity.table_col)
            self.window.table_panel.table.set_row_count(self.session_manager.session_entity.table_row)
            self.window.table_panel.table.set_headers(self.session_manager.session_entity.table_headers)
            self.window.table_panel.table.set_table_data(self.session_manager.session_entity.table_data)

            self.window.closing.connect(self.write_session_slot(session_id))

        # here logic to load data into window that we create
        # calling set functions using the qsettings object
        # QWindow parent has slot called close
        # controller has instance of session_manager created
        # session gets that data from manager and holds it in variables
        # self.window.close.connect(write_session_slot)

    @Slot()
    def write_session_slot(self, session_id):
        """
        Function that get data from the view and sends to manager.
        """

        self.session_manager.set_session_id(session_id)

        table_title = self.window.table_panel.get_table_name()
        self.session_manager.set_table_name(table_title)

        table_rows = self.window.table_panel.table.get_row_count()
        self.session_manager.set_table_rows(table_rows)

        table_cols = self.window.table_panel.table.get_col_count()
        self.session_manager.set_table_cols(table_cols)

        table_headers = self.window.table_panel.table.get_headers()
        self.session_manager.set_table_headers(table_headers)

        table_data = self.window.table_panel.table.get_table_data()
        self.session_manager.set_table_data(table_data)

        # call function to write everything to q settings
        self.session_manager.write_to_settings()

    """
        write session slot
            which gets all the data from the window
            get table name
            get row/col count
            get headers
            get table data in a list of lists
            send all to manager
    """
    """save session"""