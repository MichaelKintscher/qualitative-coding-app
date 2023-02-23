class ButtonDefinition:
    """
    An object defining the attributes for a button within the coding assistance
    panel.
    """
    def __init__(self, button, button_id, hotkey, data):
        """
        Constructor - Creates an instance of ButtonDefinition

        Parameters:
            button - button definition instance
            button_id - name of the button
            hotkey - hotkey for the button
            data - list of string data assigned to a button definition
        """
        self.button = button
        self.button_id = button_id
        self.hotkey = hotkey
        self.data = data
