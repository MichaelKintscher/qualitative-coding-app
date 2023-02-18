from PySide6.QtWidgets import QPushButton, QStyle, QWidget, QHBoxLayout


class SessionOption(QWidget):
    """
    The Session Option is a widget container for loaded sessions to be presented in the
    session manager page. The container will encapsulate buttons to manage the
    session.
    """

    def __init__(self, session_name):
        """
        Constructs an instance of the SessionOption object, declaring the
        session name and other related fields as public class members.
        """
        super().__init__()

        horizontal_layout = QHBoxLayout()

        self.remove_session_button = QPushButton()
        self.remove_session_button.setIcon(self.style().standardIcon(QStyle.SP_DialogCancelButton))
        self.session_button = QPushButton(session_name)

        horizontal_layout.addWidget(self.remove_session_button)
        horizontal_layout.addWidget(self.session_button)
        horizontal_layout.addStretch()
        self.setLayout(horizontal_layout)
