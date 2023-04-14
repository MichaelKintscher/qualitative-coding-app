class GlobalSettingsEntity:
    """
    An object containing global settings that can be applied to all sessions.
    """
    def __init__(self):
        """
        Constructor - Creates an instance of GlobalSettingsEntity
        """
        self.button_definitions = []
        self.table_padding = -1
        self.table_cell_size = [-1, -1]
        self.table_maximum_width = -1
