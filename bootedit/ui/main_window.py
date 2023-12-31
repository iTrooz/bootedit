from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from bootedit.backend.entry import UEFIEntry
from bootedit.ui.entry_table import EntryTableView
from bootedit.ui.orderable_table import OrderableTableView
from bootedit.ui import utils

# root widget
class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Boot entries editor (UEFI)")
 
        windowLayout = QVBoxLayout()
        self.setLayout(windowLayout)
 
        header = QHBoxLayout()
        windowLayout.addLayout(header)

        # add "add" button
        self.add_button = utils.gen_button(self, bundled_icon="add.svg")
        header.addWidget(self.add_button)
        
        # add "remove" button
        self.remove_button = utils.gen_button(self, bundled_icon="remove.svg")
        header.addWidget(self.remove_button)

        # put the buttons to the left by adding a spacing to the right
        header.addStretch()

        self.table = EntryTableView()
        windowLayout.addWidget(self.table)
