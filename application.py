from PyQt5.QtWidgets import QApplication

from ui.window import Window
from backend import Backend

# TODO maybe remove this class altogether
class MyApplication(QApplication):
    def __init__(self, *kargs, **kwargs):
        self.backend = Backend()
        super().__init__(*kargs, **kwargs)

    def init(self):
        self.init_ui()

    def init_ui(self):
        self.window = Window(self.backend)
        self.window.init()

    def run(self) -> int:
        self.window.show()
        return self.exec_()
