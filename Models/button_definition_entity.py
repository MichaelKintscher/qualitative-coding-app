from datetime import datetime


class ButtonDefinitionEntity:
    """
    An object defining the attributes for a button within the coding assistance
    panel.
    """
    def __init__(self, button_id, data):
        """
        Constructor - Creates an instance of ButtonDefinitionEntity

        Parameters:
            button_id - identifier of button
            data - button definition of button
        """
        self.button_id = button_id
        self.data = data
