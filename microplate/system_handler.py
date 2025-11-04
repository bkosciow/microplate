from microplate.handler_base import Handler
from microplate.handler_base import EventOnStart
from microplate.broadcast import broadcast
from microplate.message import Message
import os
import sys
import gc
from microplate.wifi import wlan
import uhashlib


class SystemHandler(Handler, EventOnStart):
    def __init__(self,):
        super().__init__()
        self.busy = False

    def handle(self, message):
        if message["event"] == "system.ping":
            fs_stats = os.statvfs("/")
            block_size = fs_stats[0]
            total_blocks = fs_stats[2]
            free_blocks = fs_stats[3]
            total = (block_size * total_blocks) // 1024
            free = (block_size * free_blocks) // 1024
            message = Message()
            message.set(
                {
                    "event": "system.pong",
                    "parameters": {
                        'name': Message.node_name,
                        'id': Message.node_id,
                        'platform': sys.platform,
                        'micropython': os.uname().release,
                        'build': os.uname().version,
                        'heap_allocated': gc.mem_alloc(),
                        'heap_free': gc.mem_free(),
                        'space_total': total,
                        'space_free': free,
                        'ip': wlan.ifconfig()
                    },
                }
            )
            broadcast(message)
            print("system.ping")

        if message["event"] == "system.microplate.get_hash":
            self.microplate_hashes()

        if message["event"] == "system.userspace.get_hash":
            self.userspace_hashes()

    def microplate_hashes(self):
        if not self.busy:
            self.busy = True
            directory = "/microplate"
            hashes = self.calculate_hash(directory)
            message = Message()
            message.set(
                {
                    "event": "system.microplate.hash",
                    "parameters": hashes,
                }
            )
            broadcast(message)
            self.busy = False
            print(hashes)

    def userspace_hashes(self):
        if not self.busy:
            self.busy = True
            directory = "/"
            hashes = self.calculate_hash(directory)
            message = Message()
            message.set(
                {
                    "event": "system.userspace.hash",
                    "parameters": hashes,
                }
            )
            broadcast(message)
            self.busy = False

    def calculate_hash(self, directory):
        hashes = {}
        try:
            for filename in os.listdir(directory):
                filepath = directory + "/" + filename if directory != "/" else filename
                if os.stat(filepath)[0] & 0x4000:  # Check if it's a directory (S_IFDIR)
                    continue
                with open(filepath, 'rb') as f:
                    hasher = uhashlib.sha256()
                    while True:
                        chunk = f.read(512)  # Read in chunks to save memory
                        if not chunk:
                            break
                        hasher.update(chunk)
                    hashes[filename] = hasher.digest().hex()
        except OSError as e:
            hashes['error'] = f"Error processing file {filepath}: {e}"
        except Exception as e:
            hashes['error'] = f"An unexpected error occurred with file {filepath}: {e}"

        return hashes

    def on_start(self):
        self.userspace_hashes()
        self.microplate_hashes()
