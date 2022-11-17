from PySide6.QtWidgets import *

class UserSettingsDialog(QDialog):
  
  def __init__(self):
  """
  Contructor: Initializes the layout of the settings dialog
  """
    super().__init__()

    dialog_layout = QVBoxLayout()
    
    encoding_table_label = QLabel("Encoding Table Settings:")
    minimum_size_hbox = QHBoxLayout()
    minimum_size_label = QLabel("Set minimum cell width and height")
    self.minimum_size_width_box = QLineEdit()
    self.minimum_size_height_box = QLineEdit()
    self.minimum_size_button = QPushButton("Change Minimum Cell Size")
    maximum_width_label = QLabel("Set maximum cell width")
    maximum_width_hbox = QHBoxLayout()
    self.maximum_width_text_box = QLineEdit()
    self.maximum_width_button = QPushButton("Set Maximum Cell Width")
    padding_label = QLabel("Set cell padding")
    padding_hbox = QHBoxLayout()
    self.padding_text_box = QLineEdit()
    self.padding_button = QPushButton("Set Padding")

    minimum_size_hbox.addWidget(self.minimum_size_width_box)
    minimum_size_hbox.addWidget(self.minimum_size_height_box)
    minimum_size_hbox.addWidget(self.minimum_size_button)
    maximum_width_hbox.addWidget(self.maximum_width_text_box)
    maximum_width_hbox.addWidget(self.maximum_width_button)
    padding_hbox.addWidget(self.padding_text_box)
    padding_hbox.addWidget(self.padding_button)

    dialog_layout.addWidget(encoding_table_label)
    
    dialog_layout.addSpacing(50)
    dialog_layout.addWidget(minimum_size_label)
    dialog_layout.addLayout(minimum_size_hbox)
    dialog_layout.addSpacing(50)
    dialog_layout.addWidget(maximum_width_label)
    dialog_layout.addLayout(maximum_width_hbox)
    dialog_layout.addSpacing(50)
    dialog_layout.addWidget(padding_label)
    dialog_layout.addLayout(padding_hbox)

    self.setLayout(dialog_layout)

  def connect_cell_size_to_slot(self, slot):
  """
  Connects a minimum_size_button event to a slot function in Controller.py
  """
    self.minimum_size_button.clicked.connect(slot)

  def connect_maximum_size_to_slot(self, slot):
  """
  Connects a maximum_width_button event to a slot function in Controller.py
  """
    self.maximum_width_button.clicked.connect(slot)

  def connect_padding_to_slot(self, slot):
  """
  Connects a padding_button event to a slot function in Controller.py
  """
    self.padding_button.clicked.connect(slot)
    
