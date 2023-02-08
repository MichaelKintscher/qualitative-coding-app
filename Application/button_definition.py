from datetime import datetime


class ButtonDefinition:
    """
    An object defining the attributes for a button within the coding assistance
    panel.
    """
    def __init__(self, button, button_id, hotkey):
        """
        Constructor - Creates an instance of ButtonDefinition
        """
        self.button = button
        self.button_id = button_id
        self.hotkey = hotkey
