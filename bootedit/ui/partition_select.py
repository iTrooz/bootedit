from typing import List

from PyQt6.QtWidgets import *

from bootedit.backend.partition_select import Disk, Partition

class PartitionSelector(QTreeWidget):
    
    def __init__(self, *kargs, **kwargs):
        super().__init__(*kargs, **kwargs)
        self.setWindowTitle("Partition selector")
        self.setHeaderHidden(True)

    def set_data(self, disks: List[Disk], default_partition: Partition):
        self.clear()

        for disk in disks:
            disk_item = QTreeWidgetItem()
            disk_item.setText(0, disk.name)
            self.addTopLevelItem(disk_item)
            disk_item.setExpanded(True)


            for partition in disk.partitions:
                part_item = QTreeWidgetItem()
                part_item.setText(0, partition.name)
                disk_item.addChild(part_item)

                if partition == default_partition:
                    part_item.setSelected(True)

