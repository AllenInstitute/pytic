import sys
import yaml
from ctypes import *
from time import sleep
from pytic_protocol import tic_constant as t_const
from pytic_structures import *
from functools import wraps
import logging

config_file = "config.yml"

usblib = windll.LoadLibrary("C:\\Users\\danc\\dev\\libusbp\\build\\libusbp-1.dll")
ticlib = windll.LoadLibrary("C:\\Users\\danc\\dev\\tic\\build\\libpololu-tic-1.dll")

logger = logging.getLogger('pytic_object')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('pytic_object.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

# [T]ic [E]rror [D]ecoder
def TED(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        e_p = func(*args, **kwargs)
        if bool(e_p):
            e = cast(e_p, POINTER(tic_error))
            logger.error(e.contents.message)
            return 1
        else:
            return 0
    return func_wrapper

def load_yaml_config():
    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    return cfg

class TicObj(object):
    def __init__(self):
        self.cfg = load_yaml_config()
        
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
    

class Tic_Device_Settings(object):
    def __init__(self):
        self.settings = tic_settings()
        self._settings_create()
        self._fill_with_defaults()
        self._load_config_settings()
        # self.apply_settings_to_device() # make automatic or on command so can be changed later?

    def _fill_with_defaults(self):
        with open(config_file, 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
        self.settings.product = t_const[cfg['settings']['product']]
        ticlib.tic_settings_fill_with_defaults(byref(self.settings))

    def apply_settings_to_device(self, device_handle):
        self._settings_fix()
        self._set_settings(device_handle)
        self._reinitialize(device_handle)

    @TED
    def _settings_fix(self):
        warnings_p = POINTER(c_char_p)()
        e_p = ticlib.tic_settings_fix(byref(self.settings),warnings_p)
        if bool(warnings_p):
            for w in warnings_p:
                logger.warning(w)
        return e_p

    @TED
    def _set_settings(self, device_handle):
        e_p = ticlib.tic_set_settings( \
            byref(device_handle), byref(self.settings))
        return e_p

    @TED
    def _settings_create(self):
        settings_p = POINTER(tic_settings)()
        e_p = ticlib.tic_settings_create(byref(settings_p))
        self._settings = settings_p[0]
        return e_p

    @TED
    def _reinitialize(self, device_handle):
        e_p = ticlib.tic_reinitialize(byref(device_handle))
        return e_p

    def _load_config_settings(self):
        with open(config_file, 'r') as ymlfile:
            cfg = yaml.load(ymlfile)

        cfg_settings = cfg['settings']
    
        setting_names = []
        setting_types = []
        for setting in self._settings._fields_:
            setting_names.append(setting[0])
            setting_types.append(setting[1])

        for setting in cfg_settings: 
            if setting in setting_names:
                value = cfg_settings[setting]
                idx = setting_names.index(setting) 
                if 'TIC' in str(value):
                    c_val = setting_types[idx](t_const[value]) 
                else:
                    c_val = setting_types[idx](value)
                setattr(self.settings, setting, c_val)

if __name__ == '__main__':
    tic = TicObj()
    tset = Tic_Device_Settings()
    print(tset.settings.product)
    print(tset.settings.current_limit)
    handle = c_int()
    print(tset.apply_settings_to_device(handle))


    # SETTINGS CONFIG FILE
    # @property
    # def product(self):
    #     product_int = ticlib.tic_settings_get_product(byref(self._settings))
    #     chklist = ["TIC_PRODUCT_T825", "TIC_PRODUCT_T834", "TIC_PRODUCT_T500"]
    #     for p in chklist:
    #         if product_int == t_const[p]:
    #             return p;
    # @product.setter
    # def product(self, product_str):
    #     ticlib.tic_settings_set_product(byref(self._settings),c_uint8(t_const[product_str]))

    # @property
    # def auto_clear_driver_error(self):
    #     return bool(ticlib.tic_settings_get_auto_clear_driver_error((byref(self._settings))))

    # @auto_clear_driver_error.setter
    # def auto_clear_driver_error(self, val_bool):
    #     ticlib.tic_settings_set_auto_clear_driver_error( \
    #         byref(self._settings), c_bool(val_bool))

    # @property
    # def ignore_error_line_high(self):
    #     return bool(ticlib.tic_settings_get_ignore_err_line_high(byref(self._settings)))

    # @ignore_error_line_high.setter
    # def ignore_error_line_high(self, val_bool):
    #         ticlib.tic_settings_set_ignore_error_line_high( \
    #         byref(self._settings), c_bool(val_bool))




