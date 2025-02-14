from ctypes import *
from .pytic_protocol import tic_constant as t_const

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
                ('polarity', c_bool)]

class tic_settings(Structure):
    _fields_ = [("product", c_uint8),
        ("firmware_version", c_uint16),
        ("control_mode", c_uint8),
        ("never_sleep", c_bool),
        ("disable_safe_start", c_bool),
        ("ignore_err_line_high", c_bool),
        ("auto_clear_driver_error", c_bool),
        ("soft_error_response", c_uint8),
        ("soft_error_position", c_int32),
        ("serial_baud_rate", c_uint32),
        ("serial_device_number", c_uint16),
        ("serial_alt_device_number", c_uint16),
        ("serial_enable_alt_device_number", c_bool),
        ("serial_14bit_device_number", c_bool),
        ("command_timeout", c_uint16),
        ("serial_crc_for_commands", c_bool),
        ("serial_crc_for_responses", c_bool),
        ("serial_7bit_responses", c_bool),
        ("serial_response_delay", c_uint8),
        ("low_vin_timeout", c_uint16),
        ("low_vin_shutoff_voltage", c_uint16),
        ("low_vin_startup_voltage", c_uint16),
        ("high_vin_shutoff_voltage", c_uint16),
        ("vin_calibration", c_int16),
        ("rc_max_pulse_period", c_uint16),
        ("rc_bad_signal_timeout", c_uint16),
        ("rc_consecutive_good_pulses", c_uint8),
        ("input_averaging_enabled", c_uint8),
        ("input_hysteresis", c_uint16),
        ("input_error_min", c_uint16),
        ("input_error_max", c_uint16),
        ("input_scaling_degree", c_uint8),
        ("input_invert", c_bool),
        ("input_min", c_uint16),
        ("input_neutral_min", c_uint16),
        ("input_neutral_max", c_uint16),
        ("input_max", c_uint16),
        ("output_min", c_int32),
        ("output_max", c_int32),
        ("encoder_prescaler", c_uint32),
        ("encoder_postscaler", c_uint32),
        ("encoder_unlimited", c_bool),
        ("pin_settings", pin_settings * t_const["TIC_CONTROL_PIN_COUNT"]),
        ("invert_motor_direction", c_bool),
        ("max_speed", c_uint32),
        ("starting_speed", c_uint32),
        ("max_accel", c_uint32),
        ("max_decel", c_uint32),
        ("current_limit", c_uint32),
        ("current_limit_during_error", c_int32),
        ("step_mode", c_uint8),
        ("decay_mode", c_uint8),
        ("auto_homing", c_bool),
        ("auto_homing_forward", c_bool),
        ("homing_speed_towards", c_uint32),
        ("homing_speed_away", c_uint32),
        ("agc_mode", c_uint8),
        ("agc_bottom_current_limit", c_uint8),
        ("agc_current_boost_steps", c_uint8),
        ("agc_frequency_limit", c_uint8),
        ("hp_enable_unrestricted_current_limits", c_bool),
        ("hp_toff", c_uint8),
        ("hp_tblank", c_uint8),
        ("hp_abt", c_bool),
        ("hp_tdecay", c_uint8),
        ("hp_decmod", c_uint8)
    ]

class pin_info(Structure):
    _fields_ = [('analog_reading', c_uint16),
                ('digital_reading', c_bool),
                ('pin_state', c_uint8)]

class tic_variables(Structure):
    _fields_ = [('product', c_uint8),
                ('operation_state', c_uint8),
                ('energized', c_bool),
                ('position_uncertain', c_bool),
                ('forward_limit_active', c_bool),
                ('reverse_limit_active', c_bool),
                ('homing_active', c_bool),
                ('error_status', c_uint16),
                ('errors_occurred', c_uint32),
                ('planning_mode', c_uint8),
                ('target_position', c_int32),
                ('target_velocity', c_int32),
                ('starting_speed', c_uint32),
                ('max_speed', c_uint32),
                ('max_decel', c_uint32),
                ('max_accel', c_uint32),
                ('current_position', c_int32),
                ('current_velocity', c_int32),
                ('acting_target_position', c_int32),
                ('time_since_last_step', c_uint32),
                ('device_reset', c_uint8),
                ('vin_voltage', c_uint32),
                ('up_time', c_uint32),
                ('encoder_position', c_int32),
                ('rc_pulse_width', c_uint16),
                ('step_mode', c_uint8),
                ('current_limit_code', c_uint8),
                ('decay_mode', c_uint8),
                ('input_state', c_uint8),
                ('input_after_averaging', c_uint16),
                ('input_after_hysteresis', c_uint16),
                ('input_after_scaling', c_int32),
                ('last_motor_driver_error', c_uint8),
                ('agc_mode', c_uint8),
                ('agc_bottom_current_limit', c_uint8),
                ('agc_current_boost_steps', c_uint8),
                ('agc_frequency_limit', c_uint8),
                ('pin_info', pin_info * t_const['TIC_CONTROL_PIN_COUNT']),
                ('last_hp_driver_errors', c_uint8)]

class tic_error(Structure):
    _fields_ = [('do_not_free', c_bool),
                ('message', c_char_p),
                ('code_count', c_size_t),
                ('code_array', POINTER(c_uint32))]
