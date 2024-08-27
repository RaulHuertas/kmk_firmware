import digitalio
from supervisor import ticks_ms

from time import sleep

from kmk.kmktime import check_deadline
from kmk.modules import Module


class Power(Module):
    def __init__(self, powersave_pin=None):
        self.enable = False
        self.powersave_pin = powersave_pin  # Powersave pin board object
        self._powersave_start = ticks_ms()
        self._usb_last_scan = ticks_ms() - 5000
        self._psp = None  # Powersave pin object
        # self._i2c = 0
        # self._i2c_deinit_count = 0
        self._loopcounter = 0

        # make_key(
        #     names=('PS_TOG',), on_press=self._ps_tog, on_release=handler_passthrough
        # )
        # make_key(
        #     names=('PS_ON',), on_press=self._ps_enable, on_release=handler_passthrough
        # )
        # make_key(
        #     names=('PS_OFF',), on_press=self._ps_disable, on_release=handler_passthrough
        # )

    def __repr__(self):
        return f'Power({self._to_dict()})'

    def _to_dict(self):
        return {
            'enable': self.enable,
            'powersave_pin': self.powersave_pin,
            '_powersave_start': self._powersave_start,
            '_usb_last_scan': self._usb_last_scan,
            '_psp': self._psp,
        }

    def during_bootup(self, keyboard):
        #self._i2c_scan()
        pass

    def before_matrix_scan(self, keyboard):
        return

    def after_matrix_scan(self, keyboard):
        if keyboard.matrix_update or keyboard.secondary_matrix_update:
            self.psave_time_reset()

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        if self.enable:
            self.psleep()

    def on_powersave_enable(self, keyboard):
        '''Gives 10 cycles to allow other extensions to clean up before powersave'''
        if self._loopcounter > 10:
            self.enable_powersave(keyboard)
            self._loopcounter = 0
        else:
            self._loopcounter += 1
        return

    def on_powersave_disable(self, keyboard):
        self.disable_powersave(keyboard)
        return

    def enable_powersave(self, keyboard):
        '''Enables power saving features'''
        #if self._i2c_deinit_count >= self._i2c and self.powersave_pin:
        if  self.powersave_pin:
            # Allows power save to prevent RGB drain.
            # Example here https://docs.nicekeyboards.com/#/nice!nano/pinout_schematic

            if not self._psp:
                self._psp = digitalio.DigitalInOut(self.powersave_pin)
                self._psp.direction = digitalio.Direction.OUTPUT
            if self._psp:
                self._psp.value = True

        self.enable = True
        keyboard._trigger_powersave_enable = False
        return

    def disable_powersave(self, keyboard):
        '''Disables power saving features'''
        if self._psp:
            self._psp.value = False
            # Allows power save to prevent RGB drain.
            # Example here https://docs.nicekeyboards.com/#/nice!nano/pinout_schematic

        keyboard._trigger_powersave_disable = False
        self.enable = False
        return

    def psleep(self):
        '''
        Sleeps longer and longer to save power the more time in between updates.
        '''
        if check_deadline(ticks_ms(), self._powersave_start, 30000):
            sleep(12 / 1000)
        elif check_deadline(ticks_ms(), self._powersave_start, 120000) is False:
            sleep(180 / 1000)
        return

    def psave_time_reset(self):
        self._powersave_start = ticks_ms()

