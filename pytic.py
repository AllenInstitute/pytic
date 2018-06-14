from ctypes import *
import numpy as np
from time import sleep

class libusbp_generic_interface(Structure):
    _fields_ = [("interface_number", c_uint8),
                ("device_instance_id", c_char_p),
                ("filename", c_char_p)]

class libusbp_generic_handle(Structure):
    # untested type, no HANDLE or WIN_INTERFACE_HANDLE type
    _fields_ = [("file_handle", c_ulong),
                ("winusb_handle", c_ulong)]

class tic_device(Structure):
    _fields_ = [("usb_interface", POINTER(libusbp_generic_interface)),
                ("serial_number", c_char_p),
                ("os_id", c_char_p),
                ("firmware_version", c_uint16),
                ("product", c_uint8)]

class tic_handle(Structure):
    _fields_ = [('usb_handle', POINTER(libusbp_generic_handle)),
                ('device', POINTER(tic_device)),
                ('cached_firmware_version_string', c_char_p)]

usblib = windll.LoadLibrary("C:\\msys64\\mingw64\\bin\\libusbp-1.dll")
ticlib = windll.LoadLibrary("C:\\Users\\danc\\dev\\tic\\build\\libpololu-tic-1.dll")

print("\nFind Connected Tic Device")
devcnt = devcnt = c_size_t(0)
dev_pp = POINTER(POINTER(tic_device))()
ticlib.tic_list_connected_devices(byref(dev_pp), byref(devcnt))
ticdev = dev_pp[0][0]
print(ticdev.serial_number)

print("\nGet Tic Device Handle")
t_handle_p = POINTER(tic_handle)()
print(ticlib.tic_handle_open(byref(ticdev), byref(t_handle_p)))
t_handle = t_handle_p[0]

print("\nRunning Motion Commands...")
print(ticlib.tic_exit_safe_start(byref(t_handle)))
print(ticlib.tic_energize(byref(t_handle)))
print(ticlib.tic_set_max_speed(byref(t_handle), c_int(6000000)))
print(ticlib.tic_set_target_velocity(byref(t_handle), c_int(5000000)))
print(ticlib.tic_halt_and_set_position(byref(t_handle), c_int(0)))
print(ticlib.tic_set_target_position(byref(t_handle), c_int(999999999999999999)))
print(ticlib.tic_reinitialize(byref(t_handle)))

# INTERNAL DEVICE CASTING, USEFUL LATER
# devchk = cast(handle_p[0].device, POINTER(tic_device))
# print(devchk.contents.serial_number)
# print(newtic.serial_number)
# print(pp)
# print(pp[0][0].serial_number)
# print(ticlib.tic_deenergize(byref(h)))
# print(ticlib.tic_set_target_velocity(byref(h),c_int(500)))

# HACKED VERSION OF CODE, REQUIRES MODIFIED SOURCE
# devcnt = c_size_t(0)
# t = pointer(c_long())

# ticlib.pytic_list_connected_devices.restype=tic_device
# ticdev = ticlib.pytic_list_connected_devices(t, byref(devcnt))
# print(ticdev)
# print(ticdev.usb_interface)
# print(ticdev.serial_number)
# print(ticdev.os_id)
# print(ticdev.firmware_version)
# print(ticdev.product)

# usbint = cast(ticdev.usb_interface, POINTER(libusbp_generic_interface))
# print(usbint.contents.interface_number)
# print(usbint.contents.device_instance_id)
# print(usbint.contents.filename)

# h_temp = pointer(c_long())

# ticlib.pytic_handle_open.restype=tic_handle
# h = ticlib.pytic_handle_open(byref(ticdev), h_temp)
# print(h)
# print(h.usb_handle)
# print(h.device)

# chk = cast(h.device, POINTER(tic_device))
# print(chk.contents.os_id)











# ticdev = tic_device()
# tp = pointer(ticdev)
# tpp = pointer(tp)
# tppp = pointer(tpp)

# t = pointer(c_long())

# print(ticlib.tic_list_connected_devices(t, byref(devcnt)))
# print(devcnt.value)

# dev_array = cast(t, POINTER(tic_device*devcnt.value))
# print(dev_array[0][0].serial_number)


# print(ticdev.os_id)
# print(ticlib.please_work_now())

# import pdb;pdb.set_trace()

# print(tp.contents.product)

# print(ticlib.tic_list_connected_devices(byref(tl), byref(devcnt)))
# ticdev_p = POINTER(tic_device) 
# tic_device_list = (ticdev_p) * 5
# tdl = tic_device_list()
# print(tl[0])
# h = cast(tl[0],POINTER(tic_device))
# print(h)
# print(h.contents.serial_number)

# tic_device_list = tic_device * 5
# tdl = tic_device_list()
# tic_list = c_ulonglong * 5
# tl = tic_list()
# t = c_ulonglong()

# usbint = libusbp_generic_interface()
# ticdev = tic_device()

# for i in range(0,1):
# print(t)
# print(t.value)
# ticdev
# for i in range(0,5):
#     print(tdl[i].serial_number)
# print(ticdev.libusbp_generic_interface)
# print(ticdev.firmware_version)
# print(ticdev.product)
# print(ticlib.tic_list_connected_devices(byref(ticdev), byref(devcnt)))
# print(ticlib.tic_list_connected_devices(byref(tdl), byref(devcnt)))