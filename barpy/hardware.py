from threading import Lock

from gpiozero import Button, LED


class BarHardware(object):
    def __init__(self):
        pass

    def num_fluids(self):
        return 0

    def pump_on(self, idx):
        pass

    def pump_off(self, idx):
        pass

    def button_is_pressed(self, idx):
        return False

    def turn_off_all_pumps(self):
        for i in range(self.num_fluids()):
            self.pump_off(i)


class BarPi(BarHardware):
    def __init__(self, pump_pins, button_pins):
        super().__init__()

        if len(pump_pins) != len(button_pins):
            raise Exception("number of pump pins does not match the number of button pins")

        self.buttons = [Button(i) for i in button_pins]
        self.pumps = [LED(i) for i in pump_pins]

    def num_fluids(self):
        return len(self.pumps)

    def pump_on(self, idx):
        self.pumps[idx].on()

    def pump_off(self, idx):
        self.pumps[idx].off()

    def button_is_pressed(self, idx):
        return self.buttons[idx].is_pressed


class BarPiZero(BarPi):
    def __init__(self, db):
        pump_pins, button_pins = db.query_pins()
        super().__init__(pump_pins, button_pins)


class TestBarHardware(BarHardware):
    def __init__(self, num_fluids):
        self.button_state = [False] * num_fluids
        self.pump_state = [False] * num_fluids

    def num_fluids(self):
        return len(self.pump_state)

    def pump_on(self, idx):
        self.pump_state[idx] = True

    def pump_off(self, idx):
        self.pump_state[idx] = False

    def button_is_pressed(self, idx):
        return self.button_state[idx]

    def button_set_pressed(self, idx, pressed):
        self.button_state[idx] = pressed


class HardwareLock(object):
    def __init__(self, hardware):
        self.__mutex = Lock()
        self.__hardware = hardware

    def __enter__(self):
        self.__mutex.acquire()
        return self.__hardware

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__mutex.release()
