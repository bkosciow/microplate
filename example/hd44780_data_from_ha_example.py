import microplate.core as core

from microplate.network_worker import NetworkWorker
from microplate.hd44780_handler import HD44780Handler
from microplate.hd44780_worker import HD44780Worker

print("booting")

# workers
net = NetworkWorker()
lcd_worker = HD44780Worker()

core.add_worker(lcd_worker)

# handlers
core.add_handler('lcd', HD44780Handler(lcd_worker))

# main loop
core.start()
