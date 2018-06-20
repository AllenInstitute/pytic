'''
PyTic - Python Interface for Pololu Tic Stepper Motor Controllers
Author: Daniel Castelli
Date: 6/18/2018
Version: 0.0.1

Status:
- error structure needed to parse command errors [priority-B]
'''

import sys
from ctypes import *
from time import sleep
from pytic_protocol import tic_constant as t_const
from pytic_structures import *

usblib = windll.LoadLibrary("C:\\Users\\danc\\dev\\libusbp\\build\\libusbp-1.dll")
ticlib = windll.LoadLibrary("C:\\Users\\danc\\dev\\tic\\build\\libpololu-tic-1.dll")

# CONNECT TO DEVICE
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
print(ticlib.tic_settings_set_auto_clear_driver_error(byref(settings), c_bool(True)))
print(ticlib.tic_settings_set_ignore_err_line_high(byref(settings),c_bool(True)))
print(ticlib.tic_settings_set_serial_crc_enabled(byref(settings),c_bool(False)))
print(ticlib.tic_settings_set_serial_crc_enabled(byref(settings),c_bool(False)))
print(ticlib.tic_settings_set_command_timeout(byref(settings),c_uint16(0)))

# Home Settings
# print(ticlib.tic_settings_set_decay_mode(byref(settings),c_uint8(t_const['TIC_DECAY_MODE_T825_SLOW'])))
# print(ticlib.tic_settings_set_step_mode(byref(settings), c_uint8(t_const['TIC_STEP_MODE_FULL'])))
# print(ticlib.tic_settings_set_max_speed(byref(settings), c_uint32(9000000)))
# print(ticlib.tic_settings_set_max_accel(byref(settings), c_uint32(3000000)))
# print(ticlib.tic_settings_set_max_decel(byref(settings), c_uint32(3000000)))

# Normal Settings
print(ticlib.tic_settings_set_decay_mode(byref(settings),c_uint8(t_const['TIC_DECAY_MODE_T825_MIXED'])))
print(ticlib.tic_settings_set_step_mode(byref(settings), c_uint8(t_const['TIC_STEP_MODE_MICROSTEP8'])))
print(ticlib.tic_settings_set_max_speed(byref(settings), c_uint32(60000000)))
print(ticlib.tic_settings_set_max_accel(byref(settings), c_uint32(50000000)))
print(ticlib.tic_settings_set_max_decel(byref(settings), c_uint32(50000000)))

# Precision Settings
# print(ticlib.tic_settings_set_decay_mode(byref(settings),c_uint8(t_const['TIC_DECAY_MODE_T825_MIXED'])))
# print(ticlib.tic_settings_set_step_mode(byref(settings), c_uint8(t_const['TIC_STEP_MODE_MICROSTEP16'])))
# print(ticlib.tic_settings_set_max_speed(byref(settings), c_uint32(120000000)))
# print(ticlib.tic_settings_set_max_accel(byref(settings), c_uint32(90000000)))
# print(ticlib.tic_settings_set_max_decel(byref(settings), c_uint32(90000000)))
print(ticlib.tic_settings_set_current_limit(byref(settings), c_uint32(1216)))
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
print("current_limit: " + str(settings.current_limit))
print(ticlib.tic_set_settings(byref(t_handle), byref(settings)))
print(ticlib.tic_reinitialize(byref(t_handle)))


# Reset after settings applied
# print(ticlib.tic_reset(byref(t_handle)))

print("\nRunning Motion Commands...")

# Homing settings
print(ticlib.tic_set_max_speed(byref(t_handle), c_uint32(60000000)))
print(ticlib.tic_set_max_accel(byref(t_handle), c_uint32(90000000)))
print(ticlib.tic_set_max_decel(byref(t_handle), c_uint32(90000000)))
#print(ticlib.tic_set_target_position(byref(t_handle), c_int32(1597*2)))
print(ticlib.tic_reset_command_timeout(byref(t_handle)))
print(ticlib.tic_set_target_velocity(byref(t_handle), c_int32(60000000)))
print(ticlib.tic_energize(byref(t_handle)))
print(ticlib.tic_exit_safe_start(byref(t_handle)))

#print(ticlib.tic_halt_and_set_position(byref(t_handle), c_int32(0)))
#print(ticlib.tic_reinitialize(byref(t_handle)))
#print(ticlib.tic_reset_command_timeout(byref(t_handle)))


sleep(3)

# Close down motor
print('slowing down')
print(ticlib.tic_set_target_velocity(byref(t_handle), c_int32(0)))
print(ticlib.tic_enter_safe_start(byref(t_handle)))
print(ticlib.tic_deenergize(byref(t_handle)))
print(ticlib.tic_clear_driver_error(byref(t_handle)))


variables_p = POINTER(tic_variables)()
print(ticlib.tic_get_variables(byref(t_handle), byref(variables_p),c_bool(True)))
variables = variables_p[0]
print(variables.product)
print(variables.error_status)
print(variables.errors_occurred)

e_bit_mask = variables.errors_occurred
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

print('e:{0:b}'.format(e_bit_mask))
for code in ecodes:
    if ((e_bit_mask >> t_const[code]) & 1):
        print("Error: " + code)

print("Locating home...")
# Pin Reading Demo
home_old = 1
for i in range(0,100):
    variables_p = POINTER(tic_variables)()
    ticlib.tic_get_variables(byref(t_handle), byref(variables_p),c_bool(True))
    variables = variables_p[0]
    home_new = ticlib.tic_variables_get_digital_reading(byref(variables),t_const['TIC_PIN_NUM_RX'])
    if not home_old == home_new:
        print("home!")
        home_old = home_new
        #tic_variables_get_current_position
    sleep(0.05)


# INTERNAL DEVICE CASTING, EXAMPLE #1
# devchk = cast(handle_p[0].device, POINTER(tic_device))
# print(devchk.contents.serial_number)

# INTERNAL DEVICE CASTING, EXAMPLE #2
# usbint = cast(ticdev.usb_interface, POINTER(libusbp_generic_interface))
# print(usbint.contents.interface_number)
# print(usbint.contents.device_instance_id)
# print(usbint.contents.filename)

# DEBUG TRACE EXAMPLE
# import pdb;pdb.set_trace()

