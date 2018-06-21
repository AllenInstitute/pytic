import sys
import yaml
from ctypes import *
from time import sleep
from pytic_protocol import tic_constant as t_const
from pytic_structures import *
from functools import wraps

usblib = windll.LoadLibrary("C:\\Users\\danc\\dev\\libusbp\\build\\libusbp-1.dll")
ticlib = windll.LoadLibrary("C:\\Users\\danc\\dev\\tic\\build\\libpololu-tic-1.dll")

# [T]ic [E]rror [D]ecoder
def TED(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        e_p = func(*args, **kwargs)
        if bool(e_p):
            e = cast(e_p, POINTER(tic_error))
            print(e.message)
            return 1
        else:
            return 0
    return func_wrapper

class TicObj(object):
    def __init__(self):
        self._settings_create()
        
    def list_connected_serial_numbers(self):
        devcnt = c_size_t(0)
        dev_pp = POINTER(POINTER(tic_device))()
        self.e_p = ticlib.tic_list_connected_devices(byref(dev_pp), byref(devcnt))
        if bool(self.e_p):
            print(self.e_p.contents.message)
        else:
            if not devcnt.value:
                print("No Tic devices connected.")
            for i in range(0, devcnt.value):
                ticdev = dev_pp[0][i]
                print("Tic Device #: {0:d}, Serial #: {1:s}".format(i, ticdev.serial_number))
    
    def load_yaml_config(self):
        pass

    @TED
    def _settings_create(self):
        settings_p = POINTER(tic_settings)()
        e_p = ticlib.tic_settings_create(byref(settings_p))
        self.settings = settings_p[0]
        return e_p

if __name__ == '__main__':
    tic = TicObj()
