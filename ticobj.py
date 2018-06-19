import sys
from ctypes import *
from time import sleep
from pytic_protocol import tic_constant as t_const
from pytic_structures import *

usblib = windll.LoadLibrary("C:\\Users\\danc\\dev\\libusbp\\build\\libusbp-1.dll")
ticlib = windll.LoadLibrary("C:\\Users\\danc\\dev\\tic\\build\\libpololu-tic-1.dll")

class TicObj(object):
    def __init__(self):
        self.error_p = POINTER(tic_error)()
        
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

if __name__ == '__main__':
    tic = TicObj()
    tic.list_connected_serial_numbers()