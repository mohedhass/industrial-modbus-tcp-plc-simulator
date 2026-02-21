from __future__ import annotations

import threading
import time
from dataclasses import dataclass

from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.server import StartTcpServer

from .process import process_loop

@dataclass
class PlcMemoryLayout:
    # Coils: 0..
    # Discrete inputs: 0..
    # Holding registers: 0..
    # Input registers: 0..
    coils_size: int = 64
    discrete_inputs_size: int = 64
    holding_registers_size: int = 64
    input_registers_size: int = 64

def run_server(host: str, port: int, unit_id: int = 1, layout: PlcMemoryLayout | None = None) -> None:
    layout = layout or PlcMemoryLayout()

    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0] * layout.discrete_inputs_size),
        co=ModbusSequentialDataBlock(0, [0] * layout.coils_size),
        hr=ModbusSequentialDataBlock(0, [0] * layout.holding_registers_size),
        ir=ModbusSequentialDataBlock(0, [0] * layout.input_registers_size),
        zero_mode=True,
    )
    context = ModbusServerContext(slaves={unit_id: store}, single=False)

    # Start background "process" simulation
    stop_event = threading.Event()
    t = threading.Thread(target=process_loop, args=(context, unit_id, stop_event), daemon=True)
    t.start()

    print(f"[PLC] Modbus TCP server listening on {host}:{port} (unit={unit_id})")
    print("[PLC] Holding register map:")
    print("  HR0  = temperature_x10 (e.g., 253 => 25.3°C)")
    print("  HR1  = setpoint_x10")
    print("  HR2  = runtime_seconds (low 16 bits)")
    print("[PLC] Coil map:")
    print("  C0 = alarm (temp > setpoint)")
    print("  C1 = heartbeat (toggles)")

    try:
        StartTcpServer(context=context, address=(host, port))
    except KeyboardInterrupt:
        print("\n[PLC] Shutting down...")
    finally:
        stop_event.set()
        time.sleep(0.2)
