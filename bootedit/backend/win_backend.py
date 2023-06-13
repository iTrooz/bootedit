from bootedit.backend.backend import Backend

class WinBackend(Backend):

    def get_uefi_entries(self) -> list[str]:
        return ["Windows Boot Manager", "GRUB", "Removable USB device", "Network boot"]
