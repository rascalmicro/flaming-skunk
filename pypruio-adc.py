#!/usr/bin/python
from pruio import *
from time import sleep

# Create a ctypes *pointer* to the pruio structure
io = pruio_new(PRUIO_DEF_ACTIVE, 0, 0, 0)
# Note the *pointer* dereferencing using the contents member
if not io.contents.Errr:
    pruio_config(io, 1, 0, 0, 0)
    reading = io.Adc.Value[1])
    print reading
    pruio_gpio_setValue(io, P8_08, i%2)
    s = pruio_Pin(io, P8_08)
    v = pruio_gpio_Value(io, P8_08)
    sleep(1)

pruio_destroy(io)

