from typing import Optional
import subprocess
import os
import tempfile

from bootedit.backend.mount.mount_error import MountError

from ..partition import Partition

def get_mount_path(partition: Partition) -> Optional[str]:
    return None

def mount(partition: Partition) -> str:
    """
    Try to mount a partition. May throw MountError if the mount fails

    :return: full path of the mount point directory
    """
    tmpdir = tempfile.mkdtemp(prefix="tmp-bootedit-")
    
    # mount in read-only can fail if the partition was already mounted in read-write elsewhere
    # If so, try to mount again in read-write mode
    # Do not do this in the 'except' block to avoid 'During handling of the above exception, another exception occurred'
    try:
        # discard output in this call. If there is really an error, it will be shown by the other call
        subprocess.check_output(["mount", partition.internal_name, tmpdir, "-t", partition.type, '-r'])
    except subprocess.CalledProcessError:
        try:
            subprocess.check_call(["mount", partition.internal_name, tmpdir, "-t", partition.type])
        except subprocess.CalledProcessError as e:
            raise MountError(e) from None

    print(f"Mounted partition {partition.internal_name} on {tmpdir}")

    return tmpdir

def unmount(partition: Partition, device_path: str):
    subprocess.check_call(["umount", device_path])
