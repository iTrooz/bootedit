from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from bootedit.logic.entry_add import EntryAddLogic

from bootedit.ui.window import Window
from bootedit.ui.entry_add import EntryAddWindow
from bootedit.backend.backend import Backend
from bootedit.backend.partition_select import get_partitions

# TODO maybe remove this class altogether
class ApplicationLogic(QApplication):
    """
    
    :attr partition_selector: widget representing the active (shown right now)
        partition selector window. None else
    """
    def __init__(self, *kargs, **kwargs):
        self.backend = Backend()
        self.partition_selector = None
        super().__init__(*kargs, **kwargs)

    def init(self):
        self.init_ui()

    def init_ui(self):
        self.window = Window(self.backend)
        self.window.init()

        self.window.add_button.clicked.connect(lambda: self.show_add_entry_window())

    def show_add_entry_window(self):
        self.entry_add = EntryAddLogic()
        self.entry_add.show_window()

    def run(self) -> int:
        self.window.show()
        return self.exec()