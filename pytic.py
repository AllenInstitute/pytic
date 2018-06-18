'''
PyTic - Python Interface for Pololu Tic Stepper Motor Controllers
Author: Daniel Castelli
Date: 6/18/2018
Version: 0.0.1
'''

import sys
from ctypes import *
from time import sleep
from pytic_protocol import tic_constant as t_const
from pytic_structures import *

usblib = windll.LoadLibrary("C:\\Users\\danc\\dev\\libusbp\\build\\libusbp-1.dll")
ticlib = windll.LoadLibrary("C:\\Users\\danc\\dev\\tic\\build\\libpololu-tic-1.dll")

print("\nFind Connected Tic Device")
devcnt = c_size_t(0)
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
settings_p = POINTER(tic_settings)()
warnings_p = POINTER(c_char_p)()
print(ticlib.tic_settings_create(byref(settings_p)))
settings = settings_p[0]
# Default Settings - must set product first
print(ticlib.tic_settings_set_product(byref(settings),c_uint8(t_const['TIC_PRODUCT_T825'])))
print(ticlib.tic_settings_fill_with_defaults(byref(settings)))
# Motion Settings
print(ticlib.tic_settings_set_step_mode(byref(settings), c_uint8(t_const['TIC_STEP_MODE_MICROSTEP8'])))
print(ticlib.tic_settings_set_max_speed(byref(settings), c_uint32(500000000)))
print(ticlib.tic_settings_set_max_accel(byref(settings), c_uint32(50000000)))
print(ticlib.tic_settings_set_current_limit(byref(settings), c_uint32(960)))
# Pin Settings - make RX digitial input pin
print(ticlib.tic_settings_set_pin_func(byref(settings),
    t_const['TIC_PIN_NUM_RX'],t_const['TIC_PIN_FUNC_USER_INPUT']))
print(ticlib.tic_settings_set_pin_pullup(byref(settings), 
    t_const['TIC_PIN_NUM_RX'], c_bool(True)))
print(ticlib.tic_settings_set_pin_analog(byref(settings), 
    t_const['TIC_PIN_NUM_RX'], c_bool(False))) 
# Apply Settings
print(ticlib.tic_settings_fix(byref(settings),warnings_p))
if bool(warnings_p):
    for warning in warnings_p:
        print(warning)
        sys.exit()
print(ticlib.tic_set_settings(byref(t_handle), byref(settings)))
print(ticlib.tic_reinitialize(byref(t_handle)))

print("\nRunning Motion Commands...")
print(ticlib.tic_exit_safe_start(byref(t_handle)))
print(ticlib.tic_energize(byref(t_handle)))
print(ticlib.tic_set_max_speed(byref(t_handle), c_uint32(500000000)))
print(ticlib.tic_set_max_accel(byref(t_handle), c_uint32(50000000)))
print(ticlib.tic_halt_and_set_position(byref(t_handle), c_int32(0)))
print(ticlib.tic_reinitialize(byref(t_handle)))
#print(ticlib.tic_reset_command_timeout(byref(t_handle)))
#print(ticlib.tic_set_target_position(byref(t_handle), c_int32(1650)))
# print(ticlib.tic_set_target_position(byref(t_handle), c_int32(1597*6)))
print(ticlib.tic_set_target_position(byref(t_handle), c_int32(1567)))
#print(ticlib.tic_set_target_velocity(byref(t_handle), c_int32(1000000)))

sleep(3)

variables_p = POINTER(tic_variables)()
print(ticlib.tic_get_variables(byref(t_handle), byref(variables_p),c_bool(True)))
variables = variables_p[0]
print(variables.product)
print(variables.error_status)
print(variables.errors_occurred)

e_bit_mask = variables.error_status
ecodes = [
    "TIC_ERROR_INTENTIONALLY_DEENERGIZED",
    "TIC_ERROR_MOTOR_DRIVER_ERROR",
    "TIC_ERROR_LOW_VIN",
    "TIC_ERROR_KILL_SWITCH",
    "TIC_ERROR_REQUIRED_INPUT_INVALID",
    "TIC_ERROR_SERIAL_ERROR",
    "TIC_ERROR_COMMAND_TIMEOUT",
    "TIC_ERROR_SAFE_START_VIOLATION",
    "TIC_ERROR_ERR_LINE_HIGH",
    "TIC_ERROR_SERIAL_FRAMING",
    "TIC_ERROR_SERIAL_RX_OVERRUN",
    "TIC_ERROR_SERIAL_FORMAT",
    "TIC_ERROR_SERIAL_CRC",
    "TIC_ERROR_ENCODER_SKIP"]
for code in ecodes:
    if (e_bit_mask & t_const[code]) == t_const[code]:
        print("Error: " + code)


# BIT MASK REQUIRED TO GET ERROR INFO FOR VARIABLE STATE
# errors_p = pointer(variables.errors_occurred)
# print(ticlib.tic_error_get_message(errors_p))
print(ticlib.tic_deenergize(byref(t_handle)))

# Pin Reading Demo
for i in range(0,3):
    variables_p = POINTER(tic_variables)()
    print(ticlib.tic_get_variables(byref(t_handle), byref(variables_p),c_bool(True)))
    variables = variables_p[0]
    print(ticlib.tic_variables_get_digital_reading(byref(variables),t_const['TIC_PIN_NUM_RX']))
    sleep(1)
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