import argparse
from .server import run_server

def main():
    ap = argparse.ArgumentParser(description="Modbus TCP PLC Simulator")
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--port", type=int, default=5020)
    ap.add_argument("--unit-id", type=int, default=1)
    args = ap.parse_args()
    run_server(host=args.host, port=args.port, unit_id=args.unit_id)

if __name__ == "__main__":
    main()
