from PySide6.QtWidgets import QGridLayout


class GridLayout(QGridLayout):
    """
    Custom QGridLayout, made to add widgets top to bottom and left to right.
    In addition, the grid row and column sizes are constant.
    """

    def __init__(self, parent, row_count, col_count):
        """
        Constructs an instance of the grid layout.

        Parameters:
            parent - pointer to the parent object the layout resides in.
            row_count - number of rows in the grid layout.
            col_count - number of columns in the grid layout.
        """
        super().__init__(parent)
        self.row_count = row_count
        self.col_count = col_count

        # Set all rows and columns to have an equal constant stretching factor.
        for row in range(self.row_count):
            self.setRowStretch(row, 1)
        for col in range(self.col_count):
            self.setColumnStretch(col, 1)

    def addWidget(self, widget):
        """
        Adds the given widget at the insertion coordinate

        Parameters:
            widget - widget to add to the layout.
        Exception:
            ValueError - unable to add widget to full layout.
        """
        current_row = 0
        current_col = 0

        while self.itemAtPosition(current_row, current_col):
            if current_col == (self.col_count - 1):
                current_col = 0
                current_row += 1
            else:
                current_col += 1

        if current_row < self.row_count and current_col < self.col_count:
            super().addWidget(widget, current_row, current_col)
        else:
            raise ValueError("Unable to add widget to GridLayout. Layout is full.")

    def removeItem(self, widget):
        """
        Removes the widget from the grid layout, shifting all elements over to fill
        the gap.

        Parameters:
            widget - widget to remove
        """
        current_row = 0
        current_col = 0
        while self.itemAtPosition(current_row, current_col) and \
                self.itemAtPosition(current_row, current_col).widget() is not widget:
            if current_col == (self.col_count - 1):
                current_col = 0
                current_row += 1
            else:
                current_col += 1

        if self.itemAtPosition(current_row, current_col) and self.itemAtPosition(current_row, current_col).widget() is widget:
            self.itemAtPosition(current_row, current_col).widget().hide()
            super().removeItem(self.itemAtPosition(current_row, current_col))
            self._shift_widgets_left(current_row, current_col)

    def widgets(self):
        """
        Returns a list of all widgets in the grid layout.

        Returns:
            List of all widgets in the grid layout.
        """
        widgets = []
        current_row = current_col = 0

        while self.itemAtPosition(current_row, current_col):
            widget = self.itemAtPosition(current_row, current_col).widget()
            widgets.append(widget)
            if current_col == (self.col_count - 1):
                current_col = 0
                current_row += 1
            else:
                current_col += 1

        return widgets

    def _shift_widgets_left(self, row, col):
        """
        Shifts all widgets following slot at given (row, col) over to the left one spot.

        Parameters:
            row - row of slot to start shifting
            col - col of slot to start shifting
        """
        current_row = row
        current_col = col

        next_row = row if col != self.columnCount() - 1 else row + 1
        next_col = col + 1 if col != self.columnCount() - 1 else 0

        while self.itemAtPosition(next_row, next_col):
            super().addWidget(self.itemAtPosition(next_row, next_col).widget(), current_row, current_col)
            self.removeItem(self.itemAtPosition(next_row, next_col))
            current_row = next_row
            current_col = next_col

            if next_col == (self.col_count - 1):
                next_col = 0
                next_row += 1
            else:
                next_col += 1
