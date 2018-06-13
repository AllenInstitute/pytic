from ctypes import *
import numpy as np

class libusbp_generic_interface(Structure):
    _fields_ = [("interface_number", c_uint8),
                ("device_instance_id", c_char_p),
                ("filename", c_char_p)]

class tic_device(Structure):
    _fields_ = [("libusbp_generic_interface", POINTER(libusbp_generic_interface)),
                ("serial_number", c_char_p),
                ("os_id", c_char_p),
                ("firmware_version", c_uint16),
                ("product", c_uint8)]

usblib = windll.LoadLibrary("C:\\msys64\\mingw64\\bin\\libusbp-1.dll")
ticlib = windll.LoadLibrary("C:\\msys64\\mingw64\\bin\\libpololu-tic-1.dll")

usbint = libusbp_generic_interface()
ticdev = tic_device()
devcnt = c_size_t(0)

tic_device_list = tic_device * 5
tdl = tic_device_list()
tic_list = c_ulonglong * 5
tl = tic_list()
t = c_ulonglong()

# print(ticlib.tic_list_connected_devices(byref(ticdev), byref(devcnt)))
# print(ticlib.tic_list_connected_devices(byref(tdl), byref(devcnt)))
print(ticlib.tic_list_connected_devices(byref(tl), byref(devcnt)))

for i in range(0,5):
     print(tl[i])
# print(t)
# print(t.value)
# ticdev

# for i in range(0,5):
#     print(tdl[i].serial_number)
# print(ticdev.libusbp_generic_interface)
# print(ticdev.firmware_version)
# print(ticdev.product)
print(devcnt.value)