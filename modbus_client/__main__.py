import argparse
from pymodbus.client import ModbusTcpClient

def _connect(host: str, port: int):
    client = ModbusTcpClient(host=host, port=port)
    if not client.connect():
        raise SystemExit(f"Could not connect to {host}:{port}")
    return client

def read_holding(args):
    c = _connect(args.host, args.port)
    rr = c.read_holding_registers(args.address, args.count, slave=args.unit_id)
    c.close()
    if rr.isError():
        raise SystemExit(f"Error: {rr}")
    print(rr.registers)

def write_holding(args):
    c = _connect(args.host, args.port)
    rr = c.write_register(args.address, args.value, slave=args.unit_id)
    c.close()
    if rr.isError():
        raise SystemExit(f"Error: {rr}")
    print("OK")

def read_coils(args):
    c = _connect(args.host, args.port)
    rr = c.read_coils(args.address, args.count, slave=args.unit_id)
    c.close()
    if rr.isError():
        raise SystemExit(f"Error: {rr}")
    print([1 if b else 0 for b in rr.bits[:args.count]])

def write_coil(args):
    c = _connect(args.host, args.port)
    rr = c.write_coil(args.address, bool(args.value), slave=args.unit_id)
    c.close()
    if rr.isError():
        raise SystemExit(f"Error: {rr}")
    print("OK")

def main():
    ap = argparse.ArgumentParser(prog="modbus_client", description="Modbus TCP Client CLI")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=5020)
    ap.add_argument("--unit-id", type=int, default=1)

    sp = ap.add_subparsers(required=True)

    p = sp.add_parser("read-holding")
    p.add_argument("--address", type=int, required=True)
    p.add_argument("--count", type=int, default=10)
    p.set_defaults(func=read_holding)

    p = sp.add_parser("write-holding")
    p.add_argument("--address", type=int, required=True)
    p.add_argument("--value", type=int, required=True)
    p.set_defaults(func=write_holding)

    p = sp.add_parser("read-coils")
    p.add_argument("--address", type=int, required=True)
    p.add_argument("--count", type=int, default=8)
    p.set_defaults(func=read_coils)

    p = sp.add_parser("write-coil")
    p.add_argument("--address", type=int, required=True)
    p.add_argument("--value", type=int, choices=[0,1], required=True)
    p.set_defaults(func=write_coil)

    args = ap.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
