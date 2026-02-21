from __future__ import annotations

import random
import time
from pymodbus.datastore import ModbusServerContext

def _get_hr(context: ModbusServerContext, unit: int, addr: int, count: int = 1):
    return context[unit].getValues(3, addr, count=count)

def _set_hr(context: ModbusServerContext, unit: int, addr: int, values):
    context[unit].setValues(3, addr, values)

def _get_co(context: ModbusServerContext, unit: int, addr: int, count: int = 1):
    return context[unit].getValues(1, addr, count=count)

def _set_co(context: ModbusServerContext, unit: int, addr: int, values):
    context[unit].setValues(1, addr, values)

def process_loop(context: ModbusServerContext, unit: int, stop_event) -> None:
    """Simple PLC-like loop: temperature drifts + alarm/heartbeat."""
    # Initialize defaults
    _set_hr(context, unit, 0, [250])  # 25.0°C
    _set_hr(context, unit, 1, [300])  # setpoint 30.0°C
    _set_hr(context, unit, 2, [0])    # runtime seconds (low 16 bits)
    _set_co(context, unit, 0, [0])    # alarm
    _set_co(context, unit, 1, [0])    # heartbeat

    start = time.time()
    heartbeat = 0
    temp = 250

    while not stop_event.is_set():
        # read setpoint from HR1 (allows client to change it)
        setpoint = _get_hr(context, unit, 1, 1)[0]

        # drift temperature with noise; clamp 15-80°C
        temp += random.randint(-2, 5)
        temp = max(150, min(800, temp))
        _set_hr(context, unit, 0, [temp])

        # runtime
        runtime = int(time.time() - start) & 0xFFFF
        _set_hr(context, unit, 2, [runtime])

        # alarm logic
        alarm = 1 if temp > setpoint else 0
        _set_co(context, unit, 0, [alarm])

        # heartbeat toggles every cycle
        heartbeat ^= 1
        _set_co(context, unit, 1, [heartbeat])

        time.sleep(0.5)
