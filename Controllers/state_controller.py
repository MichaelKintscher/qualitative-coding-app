from Controllers.project_management_controller import ProjectManagementController
from Controllers.window_controller import WindowController
from View.main_window import MainWindow
from View.project_management_window import ProjectManagementWindow


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

    def create_new_session(self, session_name, table_name="Default Title", video=None):
        """
        Creates a new window, assigning it a window controller.
        """
        if self.window:
            return

        self.window = MainWindow(session_name)
        self.window_controller = WindowController(self.window)
        self.window.show()

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
        if self.program_running:
            return

        self.create_new_session(session_id)
