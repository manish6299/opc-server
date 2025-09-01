import csv
import os
import time
from datetime import datetime, timedelta
from opcua import Client

# ===== CONFIG =====
ENDPOINT = "opc.tcp://localhost:53530/OPCUA/SimulationServer"
MAX_TAGS = 10  # how many variables to log
# ==================


def hourly_filename(now=None):
    now = now or datetime.now()
    return f"OPC_Log_{now:%Y-%m-%d_%H}.csv"


def ensure_header(path, tag_names):
    """Create CSV file with proper header if not exists."""
    if not os.path.exists(path):
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            header = ["Timestamp", "Timestamp_UTC_Epoch"]
            header += [f"Tag{i+1}_{name}" for i, name in enumerate(tag_names)]
            writer.writerow(header)


def sleep_to_next_minute():
    now = datetime.now()
    nxt = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
    time.sleep(max(0, (nxt - now).total_seconds()))


def discover_nodes(client, max_tags=MAX_TAGS):
    """Browse the Simulation folder and return exactly `max_tags` nodes, repeating if needed."""
    objects = client.get_objects_node()
    simulation = None
    for child in objects.get_children():
        if child.get_display_name().Text == "Simulation":
            simulation = child
            break

    if not simulation:
        raise RuntimeError("Simulation folder not found under Objects")

    base_nodes = simulation.get_children()

    if not base_nodes:
        raise RuntimeError("No nodes found under Simulation")

    # Repeat nodes if fewer than max_tags
    nodes, names = [], []
    while len(nodes) < max_tags:
        for n in base_nodes:
            nodes.append(n)
            names.append(n.get_display_name().Text)
            if len(nodes) == max_tags:
                break

    print(f"✅ Auto-discovered {len(nodes)} nodes:")
    for i, (n, name) in enumerate(zip(nodes, names), 1):
        print(f"  Tag{i}: {name} -> {n.nodeid}")

    return nodes, names


def main():
    while True:
        client = None
        try:
            client = Client(ENDPOINT)
            client.connect()

            nodes, names = discover_nodes(client)

            while True:
                now_local = datetime.now()
                epoch_utc = int(time.time())

                csv_path = hourly_filename(now_local)
                ensure_header(csv_path, names)

                values = []
                for n in nodes:
                    try:
                        values.append(n.get_value())
                    except Exception:
                        values.append(None)

                row = [now_local.strftime("%Y-%m-%d %H:%M:%S"), epoch_utc] + values
                with open(csv_path, "a", newline="") as f:
                    csv.writer(f).writerow(row)

                print("Wrote:", row)
                sleep_to_next_minute()

        except Exception as e:
            print("Error:", e)
            time.sleep(5)
        finally:
            try:
                if client:
                    client.disconnect()
            except:
                pass


if __name__ == "__main__":
    main()
