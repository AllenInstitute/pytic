'''
Define tic_settings structure next, then test planning mode for contant velocity operation
'''

from ctypes import *
from time import sleep

T_CONST = {'TIC_CONTROL_PIN_COUNT': 5}

TIC_CONTROL_PIN_COUNT = 5
TIC_PRODUCT_T825 = 1
TIC_RESPONSE_GO_TO_POSITION = 3
TIC_STEP_MODE_MICROSTEP8 = 3

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

class pin_settings(Structure):
    _fields_ = [('func', c_uint8),
                ('pullup', c_bool),
                ('analog', c_bool),
                ('polarity', c_bool)];

class tic_settings(Structure):
    _fields_ = [('product', c_uint8),
                ('control_mode', c_uint8),
                ('never_sleep', c_bool),
                ('disable_safe_start', c_bool),
                ('ignore_err_line_high', c_bool),
                ('auto_clear_driver_error', c_bool),
                ('soft_error_response', c_uint8),
                ('soft_error_position', c_int32),
                ('serial_baud_rate', c_uint32),
                ('serial_device_number', c_uint8),
                ('command_timeout', c_uint16),
                ('serial_crc_enabled', c_bool),
                ('serial_response_delay', c_uint8),
                ('low_vin_timeout', c_uint16),
                ('low_vin_shutoff_voltage', c_uint16),
                ('low_vin_startup_voltage', c_uint16),
                ('high_vin_shutoff_voltage', c_uint16),
                ('vin_calibration', c_int16),
                ('rc_max_pulse_period', c_uint16),
                ('rc_bad_signal_timeout', c_uint16),
                ('rc_consecutive_good_pulses', c_uint8),
                ('input_averaging_enabled', c_uint8),
                ('input_hysteresis', c_uint16),
                ('input_error_min', c_uint16),
                ('input_error_max', c_uint16),
                ('input_scaling_degree', c_uint8),
                ('input_invert', c_bool),
                ('input_min', c_uint16),
                ('input_neutral_min', c_uint16),
                ('input_neutral_max', c_uint16),
                ('input_max', c_uint16),
                ('output_min', c_int32),
                ('output_max', c_int32),
                ('encoder_prescaler', c_uint32),
                ('encoder_postscaler', c_uint32),
                ('encoder_unlimited', c_bool),
                ('pin_settings', pin_settings * TIC_CONTROL_PIN_COUNT),
                ('current_limit', c_uint32),
                ('current_limit_during_error', c_int32),
                ('step_mode', c_uint8),
                ('decay_mode', c_int8),
                ('starting_speed', c_uint32),
                ('max_speed', c_uint32),
                ('max_decel', c_uint32),
                ('max_accel', c_uint32),
                ('invert_motor_direction', c_bool)]

usblib = windll.LoadLibrary("C:\\Users\\danc\\dev\\libusbp\\build\\libusbp-1.dll")
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

print("\nSettings related...")
# CODE FUNCTIONAL, BUT BURNS EEPROM, DON'T RUN EVERYTIME
# settings_p = POINTER(tic_settings)()
# print(ticlib.tic_settings_create(byref(settings_p)))
# settings = settings_p[0]
# print(ticlib.tic_settings_set_product(byref(settings),c_uint8(TIC_PRODUCT_T825)))
# print(ticlib.tic_settings_fill_with_defaults(byref(settings)))
# print(ticlib.tic_settings_set_command_timeout(byref(settings), c_uint16(0)))
# print(ticlib.tic_settings_set_step_mode(byref(settings), c_uint8(TIC_STEP_MODE_MICROSTEP8)))

print("\nRunning Motion Commands...")
print(ticlib.tic_exit_safe_start(byref(t_handle)))
print(ticlib.tic_energize(byref(t_handle)))
print(ticlib.tic_set_max_speed(byref(t_handle), c_uint32(1000000)))
print(ticlib.tic_set_max_accel(byref(t_handle), c_uint32(6000000)))
print(ticlib.tic_halt_and_set_position(byref(t_handle), c_int32(0)))
print(ticlib.tic_reinitialize(byref(t_handle)))
#print(ticlib.tic_reset_command_timeout(byref(t_handle)))
#print(ticlib.tic_set_target_position(byref(t_handle), c_int32(1650)))
print(ticlib.tic_set_target_position(byref(t_handle), c_int32(1597*6)))
#print(ticlib.tic_set_target_velocity(byref(t_handle), c_int32(1000000)))

sleep(3)

print(ticlib.tic_deenergize(byref(t_handle)))


# INTERNAL DEVICE CASTING, USEFUL LATER
# devchk = cast(handle_p[0].device, POINTER(tic_device))
# print(devchk.contents.serial_number)
# print(newtic.serial_number)
# print(pp)
# print(pp[0][0].serial_number)
# print(ticlib.tic_deenergize(byref(h)))
# print(ticlib.tic_set_target_velocity(byref(h),c_int(500)))

# TRACE COMMANDS - DEBUG
# import pdb; pdb.set_trace()

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

#print(ticlib.tic_settings_get_serial_baud_rate(byref(settings)))
#print(ticlib.tic_settings_set_command_timeout(byref(settings),c_uint16(60000)))
#print(settings.command_timeout)
#print(ticlib.tic_settings_set_soft_error_response(byref(settings), c_uint8(TIC_RESPONSE_GO_TO_POSITION)))

# print(ticlib.tic_settings_free(byref(settings)))
# print(ticlib.tic_settings_set_product(byref(settings),c_uint8(TIC_PRODUCT_ID_T825)))
# print(ticlib.tic_settings_fill_with_defaults(byref(settings)))
# print(settings.product)
# print(settings.serial_baud_rate)