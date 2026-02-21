# Industrial Modbus TCP PLC Simulator (Python)

A lightweight **Modbus TCP server** that simulates PLC coils/registers and a small **client CLI** to read/write values.
Designed for portfolio demos and industrial comms practice.

## What it demonstrates
- Modbus TCP basics (coils, discrete inputs, holding/input registers)
- Simple PLC-style process simulation loop
- Client tooling + clean repo structure

## Quick start (local)

### 1) Create venv + install
```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows
# .venv\Scripts\activate

pip install -r requirements.txt
```

### 2) Run the Modbus server (simulated PLC)
```bash
python -m plc_server --host 0.0.0.0 --port 5020
```

### 3) In another terminal, use the client CLI
Read 10 holding registers starting at address 0:
```bash
python -m modbus_client read-holding --host 127.0.0.1 --port 5020 --address 0 --count 10
```

Write holding register 0 to value 1234:
```bash
python -m modbus_client write-holding --host 127.0.0.1 --port 5020 --address 0 --value 1234
```

Read/write coil 0:
```bash
python -m modbus_client read-coils --host 127.0.0.1 --port 5020 --address 0 --count 8
python -m modbus_client write-coil --host 127.0.0.1 --port 5020 --address 0 --value 1
```

## Simulated process model (simple)
The server runs a loop that:
- increments a “temperature” register with noise
- toggles an “alarm” coil if temperature exceeds a threshold
- provides a heartbeat coil

You can change the logic in `plc_server/process.py`.

## Repo structure
```
industrial-modbus-tcp-simulator/
  plc_server/
    __init__.py
    __main__.py
    process.py
  modbus_client/
    __init__.py
    __main__.py
  requirements.txt
  LICENSE
```

## Notes
- Uses TCP port **5020** by default (non-privileged). Port 502 may require admin privileges.
- For real PLC integration, you'd point a SCADA/HMI or test client at the server IP/port.

## License
MIT
