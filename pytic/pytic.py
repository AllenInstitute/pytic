import sys
import os
import yaml
from ctypes import *
from time import sleep
from .pytic_protocol import tic_constant as tc
from .pytic_structures import *
from functools import wraps, partial
import logging

# [T]ic [E]rror [D]ecoder
def TED(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        _e_p = func(*args, **kwargs)
        if bool(_e_p):
            _e = cast(_e_p, POINTER(tic_error))
            _logger = logging.getLogger('PyTic')
            _logger.error(_e.contents.message)
            return 1
        else:
            return 0
    return func_wrapper

class PyTic(object):
    def __init__(self, log_file=None):
        self._load_drivers()
        self._logger = self._initialize_logger()
        self.device = None
        self.handle = None
        self.settings = None
        self.variables = None
        self._commands = [('set_target_position', c_int32),
                          ('set_target_velocity', c_int32),
                          ('halt_and_set_position', c_int32),
                          ('halt_and_hold', None),
                          ('reset_command_timeout', None),
                          ('deenergize', None),
                          ('energize', None),
                          ('exit_safe_start', None),
                          ('enter_safe_start', None),
                          ('reset', None),
                          ('clear_driver_error', None),
                          ('set_max_speed', c_uint32),
                          ('set_starting_speed', c_uint32),
                          ('set_max_accel', c_uint32),
                          ('set_max_decel', c_uint32),
                          ('set_step_mode', c_uint8),
                          ('set_current_limit', c_uint32),
                          ('set_current_limit_code', c_uint8),
                          ('set_decay_mode', c_uint8)]
        self._create_tic_command_attributes()

    def _initialize_logger(self):
        # - Logging - 
        self._log_level = logging.DEBUG
        _logger = logging.getLogger('PyTic')
        _logger.setLevel(self._log_level)
        _formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # Console Logging
        _ch = logging.StreamHandler()
        _ch.setLevel(self._log_level)
        _ch.setFormatter(_formatter)
        _logger.addHandler(_ch)
        return _logger
    
    @property
    def log_level(self):
        return self._log_level

    @log_level.setter
    def log_level(self, level):
        self._log_level = level
        self._logger.setLevel(level)

    def _load_drivers(self):
        # Driver Locations (x64)
        file_path = os.path.dirname(os.path.abspath(__file__))
        #file_path = file_path[:-len('pytic')]
        self.usblib = windll.LoadLibrary(file_path+"\\drivers\\x64\\libusbp-1.dll")
        self.ticlib = windll.LoadLibrary(file_path+"\\drivers\\x64\\libpololu-tic-1.dll")

    def _create_tic_command_attributes(self):
        for c in self._commands:
            if bool(c[1]):
                setattr(self.__class__, c[0], partial(self._tic_command_with_value, c[0], c[1]))
            else:
                setattr(self.__class__, c[0], partial(self._tic_command, c[0]))

    @TED
    def _tic_command(self, cmd_name):
        e_p = getattr(self.ticlib,'tic_'+ cmd_name)(byref(self.handle))
        return e_p

    @TED
    def _tic_command_with_value(self, cmd_name, c_type, value):
        if 'TIC' in str(value):
            value = tc[value]
        e_p = getattr(self.ticlib,'tic_'+ cmd_name)(byref(self.handle), c_type(value))
        return e_p

    @TED
    def _list_connected_devices(self):
        self._devcnt = c_size_t(0)
        self._dev_pp = POINTER(POINTER(tic_device))()
        e_p = self.ticlib.tic_list_connected_devices(byref(self._dev_pp), byref(self._devcnt))
        return e_p

    @TED
    def _tic_handle_open(self):
        handle_p = POINTER(tic_handle)()
        e_p = self.ticlib.tic_handle_open(byref(self.device), byref(handle_p))
        self.handle = handle_p[0]
        return e_p

    def list_connected_device_serial_numbers(self):
        self._list_connected_devices()
        tic_list = []
        if not self._devcnt.value:
            print("No Tic devices connected.")
        for i in range(0, self._devcnt.value):
            ticdev = self._dev_pp[0][i]
            tic_list.append(ticdev.serial_number.decode('utf-8'))
            # print("Tic Device #: {0}, Serial #: {1}".format(i, sn))
        return tic_list

    def connect_to_serial_number(self, serial_number):
        self._list_connected_devices()
        for i in range(0, self._devcnt.value):
            if serial_number == self._dev_pp[0][i].serial_number.decode('utf-8'):
                self.device = self._dev_pp[0][i]
                self._tic_handle_open()
                self.variables = PyTic_Variables(self.handle, (self.usblib, self.ticlib))
                self.settings = PyTic_Settings(self.handle, (self.usblib, self.ticlib), self.variables.product)
                return 0
        if not self.device:
            self._logger.error("Serial number device not found.")
            return 1


class PyTic_Variables(object):
    def __init__(self, device_handle, driver_handles):
        self.usblib, self.ticlib = driver_handles
        self._logger = logging.getLogger('PyTic') 
        self._device_handle = device_handle
        self._tic_variables_p = POINTER(tic_variables)()
        self._tic_variables = tic_variables()
        
        self.pin_info = []
        for i in range(0, tc['TIC_CONTROL_PIN_COUNT']):
            self.pin_info.append(type('pinfo_'+str(i), (object,), {})())

        self._convert_structure_to_readonly_properties()

    def _convert_structure_to_readonly_properties(self):
        for field in tic_variables._fields_:
            if not field[0] == 'pin_info':
                prop = property(fget=partial(self._get_tic_readonly_property, field[0]))
                setattr(self.__class__, field[0], prop)
        
        for i in range(0, tc['TIC_CONTROL_PIN_COUNT']):
            for field in pin_info._fields_:
                prop = property(fget=partial(self._get_pin_readonly_property, field[0], i))
                setattr(self.pin_info[i].__class__, field[0], prop)

    @TED
    def _update_tic_variables(self):
        e_p = self.ticlib.tic_get_variables(byref(self._device_handle), \
                                       byref(self._tic_variables_p), c_bool(True))
        self._tic_variables = self._tic_variables_p[0]
        return e_p

    def _get_tic_readonly_property(self, field, obj):
        self._update_tic_variables()
        value = getattr(self._tic_variables, field)
        if field == "error_status" or field == "error_occurred":
            self._convert_error_bitmask(value)
        return value

    def _get_pin_readonly_property(self, field, pin_num, obj):
        self._update_tic_variables()
        return getattr(self._tic_variables.pin_info[pin_num], field)

    def _convert_error_bitmask(self, e_bit_mask):
        ecodes = ["TIC_ERROR_INTENTIONALLY_DEENERGIZED",
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
            if ((e_bit_mask >> tc[code]) & 1):
                self._logger.error(code)

        
class PyTic_Settings(object):
    def __init__(self, device_handle, driver_handles, product):
        self.usblib, self.ticlib = driver_handles
        self._logger = logging.getLogger('PyTic')
        self._device_handle = device_handle
        # local vs device - local settings on pc, device settings on tic
        self._local_settings = tic_settings()
        self._device_settings = tic_settings()
        self._device_settings_p = POINTER(tic_settings)()
        
        self.pin_settings = []
        for i in range(0, tc['TIC_CONTROL_PIN_COUNT']):
            self.pin_settings.append(type('pset_'+str(i), (object,), {})())
        
        self._convert_structure_to_properties()
        self.auto_apply = False

        if "TIC" in str(product):
            product = int(tc[product])
        self._fill_with_defaults(product)

    def _convert_structure_to_properties(self):
        for field in tic_settings._fields_:
            if not field[0] == 'pin_settings':
                prop = property(fget=partial(self._get_tic_settings_from_device, field[0]),
                                fset=partial(self._set_tic_settings_with_option, field[0]))
                setattr(self.__class__, field[0], prop)

        for i in range(0, tc['TIC_CONTROL_PIN_COUNT']):
            for field in pin_settings._fields_:
                prop = property(fget=partial(self._get_pin_settings_from_device, field[0], i),
                                fset=partial(self._set_pin_settings_with_option, field[0], i))
                setattr(self.pin_settings[i].__class__, field[0], prop)

    def _get_tic_settings_from_device(self, field, obj):
        self._pull_device_settings()
        return getattr(self._device_settings, field)

    def _set_tic_settings_with_option(self, field, obj, value):
        setattr(self._local_settings, field, value)
        if (self.auto_apply):
            self.apply()

    def _get_pin_settings_from_device(self, field, pin_num, obj):
        self._pull_device_settings()
        return getattr(self._device_settings.pin_settings[pin_num], field)

    def _set_pin_settings_with_option(self, field, pin_num, obj, value):
        setattr(self._local_settings.pin_settings[pin_num], field)
        if (self.auto_apply):
            self.apply()

        
    @TED
    def _pull_device_settings(self):
        e_p = self.ticlib.tic_get_settings(byref(self._device_handle),
                                      byref(self._device_settings_p))
        self._device_settings = self._device_settings_p[0]
        return e_p

    @TED
    def _set_settings(self):
        e_p = self.ticlib.tic_set_settings(byref(self._device_handle),
                                      byref(self._local_settings))
        return e_p
        
    def _fill_with_defaults(self, product):
        self._local_settings.product = product
        self.ticlib.tic_settings_fill_with_defaults(byref(self._local_settings))

    def apply(self):
        self._settings_fix()
        self._set_settings()
        self._reinitialize()

    @TED
    def _settings_fix(self):
        warnings_p = POINTER(c_char_p)()
        e_p = self.ticlib.tic_settings_fix(byref(self._local_settings),warnings_p)
        if bool(warnings_p):
            for w in warnings_p:
                self._logger.warning(w)
        return e_p

    @TED
    def _reinitialize(self):
        e_p = self.ticlib.tic_reinitialize(byref(self._device_handle))
        return e_p

    def load_config(self, config_file):
        with open(config_file, 'r') as ymlfile:
            cfg = yaml.load(ymlfile)

        cfg_settings = cfg['tic_settings']

        tic_settings_list = []
        for setting in tic_settings._fields_:
            tic_settings_list.append(setting[0])

        for setting in cfg_settings: 
            if setting in tic_settings_list:
                if setting == 'pin_settings':
                    for pin in cfg_settings['pin_settings']:
                        i = tc[pin['pin_num']]
                        if 'func' in pin:
                            self._local_settings.pin_settings[i].func = tc[pin['func']]
                        if 'pullup' in pin:
                            self._local_settings.pin_settings[i].pullup = pin['pullup']
                        if 'analog' in pin:
                            self._local_settings.pin_settings[i].analog = pin['analog']
                        if 'polarity' in pin:
                            self._local_settings.pin_settings[i].polarity = pin['polarity']
                else:
                    if 'TIC' in str(cfg_settings[setting]):
                        value = tc[cfg_settings[setting]]
                    else:
                        value = cfg_settings[setting]
                    setattr(self._local_settings, setting, value)

        if (self.auto_apply):
            self.apply()

if __name__ == '__main__':

    tic = PyTic()
    print(tic.list_connected_device_serial_numbers())