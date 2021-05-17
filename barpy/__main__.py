import argparse
import datetime

from time import sleep
from threading import Thread

from .server import Server
from .hardware import HardwareLock, BarPiZero, TestBarHardware
from .api import app
from .db import DB


class ButtonThread(Thread):
    def __init__(self, lhw, server):
        super().__init__(daemon=True)
        self.lhw = lhw
        self.server = server

        with self.lhw as hardware:
            self.on_start = [None] * hardware.num_fluids()

    def run(self):
        while not self.server.is_done():
            with self.lhw as hardware:
                for i in range(hardware.num_fluids()):
                    if hardware.button_is_pressed(i):
                        if self.on_start[i] is None:
                            print("%d on" % i)
                            self.on_start[i] = datetime.datetime.now()
                            hardware.pump_on(i)
                    else:
                        if self.on_start[i] is not None:
                            start = self.on_start[i]
                            self.on_start[i] = None
                            diff = datetime.datetime.now() - start
                            print("%d off after %f seconds" % (i, diff.total_seconds()))
                            hardware.pump_off(i)
            sleep(0.1)


parser = argparse.ArgumentParser(description='Barpy is a server which interfaces with a BarPi')
parser.add_argument('--debug-hardware', dest='hardware', action='store_const', const='debug', default='rpi_zero')
args = parser.parse_args()

db = DB()

if args.hardware == 'debug':
    print("Running on debug hardware")
    locked_hardware = HardwareLock(TestBarHardware(6))
else:
    locked_hardware = HardwareLock(BarPiZero(), db)

app.init(db, locked_hardware)
server = Server(app)
t = ButtonThread(locked_hardware, server)
t.start()

try:
    app.run(host='0.0.0.0', port=80)
except KeyboardInterrupt:
    server.shutdown()
