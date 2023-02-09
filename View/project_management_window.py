import sys

import PySide6
from PySide6.QtWidgets import QStackedWidget

from View.session_creator_page import SessionCreatorPage
from View.session_manager_page import SessionManagerPage


class ProjectManagementWindow(QStackedWidget):
    """ Container for all project management pages. """
    def __init__(self):
        """ Constructs the window, adding all project management pages to the window. """
        super().__init__()

        session_manager_page = SessionManagerPage()
        session_creator_page = SessionCreatorPage()

        self.addWidget(session_manager_page)
        self.addWidget(session_creator_page)

        # Set width and height of window to half the screen width and height.
        screen_size = PySide6.QtGui.QGuiApplication.primaryScreen().size().toTuple()
        self.resize(screen_size[0] * 0.5, screen_size[1] * 0.5)

        # Move the window to the center of the screen
        self.move(PySide6.QtGui.QGuiApplication.primaryScreen().availableGeometry().center() - self.rect().center())

    def get_widget(self, index):
        """
        Gets the widget at the specified index

        Parameters:
            index: the index of the widget to get

        Return:
            reference to the widget of the specified index, None if not found.
        """
        if index < 0 or index > self.count():
            return None

        return self.widget(index)

    def set_current_widget(self, index):
        """
        Sets the current widget to be displayed in the window.

        Parameters:
            index: The index of the page to display
        """
        if index < 0 or index > self.count():
            print("Error: Invalid page index")
            sys.exit(-1)

        self.setCurrentIndex(index)


