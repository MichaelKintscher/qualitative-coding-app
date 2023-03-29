class GlobalSettingsEntity:
    """
    An object containing global settings that can be applied to all sessions.
    """
    def __init__(self):
        """
        Constructor - Creates an instance of GlobalSettingsEntity
        """
        self.button_definitions = []
        self.table_padding = 0
        self.table_cell_size = []
        self.table_maximum_width = 0
        self.table_font_size = 1
