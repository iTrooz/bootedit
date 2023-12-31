from typing import Optional

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt

from firmware_variables import get_boot_order, set_boot_order, adjust_privileges

from bootedit.backend.entry import UEFIEntry, get_uefi_entries
from bootedit.backend.fv_ext.delete_boot_entry import delete_boot_entry
from bootedit.backend.partition import get_partitions, get_current_guid
from bootedit.ui.main_window import MainWindow
from bootedit.ui_logic.add_uefi_entry import AddUEFIEntryLogic

class MainWindowLogic:
    """
    Logic for the main window (and kinda the whole application)
    
    :attr partition_selector: widget representing the active (shown right now)
        partition selector window. None else
    """
    def __init__(self):
        self.init_ui()

    def init_ui(self):
        self.main_window = MainWindow()
        self.reload_entries()

        self.main_window.add_button.clicked.connect(lambda: self.show_add_entry_window())

        self.main_window.remove_button.clicked.connect(lambda: self.remove_selected_entry())

        self.main_window.table.row_moved.connect(self.entry_moved)

    def remove_selected_entry(self) -> None:


        current_index = self.main_window.table.currentIndex()
        entry: Optional[UEFIEntry] = None
        if current_index:
            item = self.main_window.table.model().item(current_index.row(), 0)
            if hasattr(item, "entry"):
                entry = item.entry
        
        if not entry:
            print("Warning: No entry selected")
            return
        
        SB = QMessageBox.StandardButton
        ret = QMessageBox.question(self.main_window, "", f"Are you sure you want to remove the entry '{entry.name}' ?", SB.Yes | SB.No)
        if ret ==  SB.Yes:
            delete_boot_entry(entry.id)

            self.reload_entries()


    def reload_entries(self) -> None:
        self.set_entries(get_uefi_entries())

    def show_add_entry_window(self):
        self.add_entry_window = AddUEFIEntryLogic()
        
        partitions = get_partitions()

        with adjust_privileges():
            default_guid = get_current_guid()
        
        self.add_entry_window.set_partitions_data(partitions, default_guid)
        self.add_entry_window.show_window()
        self.add_entry_window.close_event = self.on_close_add_entry_window

    def on_close_add_entry_window(self, *_) -> None:
        self.reload_entries()


    def show_window(self):
        self.main_window.show()

    def entry_moved(self):
        new_order = []
        for row in range(self.main_window.table.model().rowCount()):
            item = self.main_window.table.model().item(row, 0)
            entry: UEFIEntry = item.entry
            new_order.append(entry.id)

        with adjust_privileges():
            old_order = get_boot_order()
            
            # Juuust to be sure
            assert sorted(old_order) == sorted(new_order)

            set_boot_order(new_order)

    def set_entries(self, entries: list[UEFIEntry]) -> None:
        self.main_window.table.clear_rows()

        for entry in entries:
            self.main_window.table.add_entry(entry)
            