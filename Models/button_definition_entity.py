from datetime import datetime


class ButtonDefinitionEntity:
    """
    An object defining the attributes for a button within the coding assistance
    panel.
    """
    def __init__(self, button_id, hotkey, data):
        """
        Constructor - Creates an instance of ButtonDefinitionEntity
        """
        self.button_id = button_id
        self.hotkey = hotkey
        self.data = data
