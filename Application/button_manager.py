class ButtonManager:
    """
    ButtonManager is a manager for the current session that saves all
    active button hotkeys and button definitions. It also provides
    functionality to save the button data to file, using QSettings.
    """

    def __init__(self):
        """
        Constructs an instance of the ButtonManager manager class.
        """
        self.hotkey_map = {}      # id : hotkey
        self.definition_map = {}  # id : button definition

    def add_button_definition(self, identifier, button_definition):
        """
        Maps the button identifier to its button definition in storage.

        Parameters:
            identifier - identifier of button
            button_definition - definition of button
        """
        self.definition_map[identifier] = button_definition

    def add_button_hotkey(self, identifier, hotkey):
        """
        Maps the button identifier to its hotkey

        Parameters:
            identifier - identifier of button
            hotkey - hotkey of button
        """
        self.hotkey_map[identifier] = hotkey

    def get_button_data(self):
        """
        Get a list of all active encoding button data.

        Returns:
            List of (hotkey, definition) pairs of all active encoding buttons.
        """
        button_data = []
        for identifier in self.hotkey_map.keys():
            button_data_pair = (self.hotkey_map[identifier], self.definition_map[identifier])
            button_data.append(button_data_pair)
        return button_data

    def get_hotkeys(self):
        """
        Gets all active hotkeys for encoding buttons

        Returns:
            List of all active hotkeys
        """
        return list(self.hotkey_map.values())

    def remove_button_definition(self, identifier):
        """
        Removes the definition associated to the given button identifier.

        Parameters:
            identifier - identifier of button to remove definition of.
        """
        del self.definition_map[identifier]

    def remove_button_hotkey(self, identifier):
        """
        Removes the hotkey associated to the given button identifier.

        Parameters:
            identifier - identifier of button to remove hotkey of.
        """
        del self.hotkey_map[identifier]
