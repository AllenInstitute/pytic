<!-- Falcon Optics Readme -->
# PyTic v0.0.2   

![pololu tic](images/pololu_tic.png)

---

## Introduction

`PyTic` is an object-oriented Python wrapper for the Pololu Tic stepper driver series. The wrapper interacts with the stepper driver device using the API described in the [pololu-tic-software][pololu_tic_software] GitHub page using the ctypes library. The comunication protocol is USB.


---

## Installation

To install the `PyTic` package on a Windows machine equipped with Python 2.7 or higher, run the following `pip` command:

```console
C:\> pip install pytic
```

* Note: Only Windows x64 machines are supported at this time.

---

## Public Methods & Properties

`PyTic` encompasses almost all functionality present in the original C-API with some additional features. The Pololu Tic stepper driver is represented in Python using a `pytic.PyTic()` object. Below are some of the highlighted public methods and properties for interacting with the device. Users can follow the same syntax and reference the [Pololu Tic Manual][pololu_tic_manual] for a list of all possible commands.

```
----------------------------------
|     Package Relation Tree      |
----------------------------------

PyTic               [Object]
  |-- Settings      [Structure]
  |-- Variables     [Structure]
  |-- Logger        [Notification]

PyTic_Protocol      [Constants]
```

### Error Handling

All __Pololu Tic C-API__ functions when dynamically imported into __PyTic__ are wrapped in a higher-order function error handler called __TED__, short for __[T]ic [E]rror [D]ecoder__. __TED__ will make all Tic wrapped functions return 0 from a successful call and 1 from a call that generated an error. In addition, __TED__ performs low-level bit mask decoding and writes the the enumerated error value to the __PyTic__ object internal log. This log can be output the ther terminal or file using the standard [logging][logging_lib] library.

---

## Example Code

The example code below deomnstrates how to connect to a __Pololu Tic__ device over USB and move to several positions after the previous position has been reached. 

```python
import pytic
from time import sleep

# - Initialization -------------------------------------------

tic = pytic.PyTic()

# Connect to first available Tic Device serial number over USB
serial_nums = tic.list_connected_device_serial_numbers()
tic.connect_to_serial_number(serial_nums[0])

# Load configuration file and apply settings
tic.settings.load_config('path\\to\\config.yml')
tic.settings.apply()                              # See Notes

# - Motion Command Sequence ----------------------------------

# Zero current motor position
tic.halt_and_set_position(0)

# Energize Motor
tic.energize()
tic.exit_safe_start()

# Move to listed positions
positions = [1000, 2000, 3000, 0]
for p in positions:
  tic.set_target_position(p)
  while tic.variables.current position != tic.variables.target_position:
    sleep(0.1)

# De-energize motor and get error status
tic.enter_safe_start()
tic.deenergize()
tic.variables.error_status()
```

* Note: Modified settings will not take effect until `PyTic.settings.apply()` method is called. This is to avoid unnecessary writes to non-volitile memory.

## Example YAML Configuration File


---

## Dependencies

Dependencies include the following,

* PyYAML

---

## External Resources

External resources include the following,

* [Pololu-Tic-Software GitHub][pololu_tic_software]
* [Pololu Tic Manual][pololu_tic_manual]

[pololu_tic_software]: https://github.com/pololu/pololu-tic-software
[pololu_tic_manual]: https://www.pololu.com/docs/0J71
[logging_lib]: https://docs.python.org/3/library/logging.html