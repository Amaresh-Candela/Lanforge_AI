from agent.runtime_manager import RuntimeManager

manager = RuntimeManager()

host = input("LANForge IP : ")

runtime = manager.connect(host)

print("\n" + "=" * 80)
print("LANFORGE RUNTIME")
print("=" * 80)

print(f"Connected  : {runtime.connected}")
print(f"Host       : {runtime.host}")

print()

print(f"Stations   : {len(runtime.stations)}")
print(f"Radios     : {len(runtime.radios)}")
print(f"Ethernet   : {len(runtime.ethernet)}")
print(f"Interfaces : {len(runtime.interfaces)}")

print("\n" + "=" * 80)
print("STATIONS")
print("=" * 80)

for eid, info in runtime.stations.items():

    print(f"""
EID       : {eid}
Alias     : {info.get("alias")}
IP        : {info.get("ip")}
MAC       : {info.get("mac")}
SSID      : {info.get("ssid")}
Channel   : {info.get("channel")}
Signal    : {info.get("signal")}
Security  : {info.get("security")}
Status    : {info.get("status")}
""")

print("\n" + "=" * 80)
print("RADIOS")
print("=" * 80)

for eid, info in runtime.radios.items():

    print(f"""
EID       : {eid}
Alias     : {info.get("alias")}
Channel   : {info.get("channel")}
Mode      : {info.get("mode")}
MAC       : {info.get("mac")}
Hardware  : {info.get("hardware")}
""")

print("\n" + "=" * 80)
print("ETHERNET")
print("=" * 80)

for eid, info in runtime.ethernet.items():

    print(f"""
EID       : {eid}
Alias     : {info.get("alias")}
IP        : {info.get("ip")}
MAC       : {info.get("mac")}
TX Rate   : {info.get("tx-rate")}
RX Rate   : {info.get("rx-rate")}
Gateway   : {info.get("gateway ip")}
""")

print("\n" + "=" * 80)
print("ALL INTERFACES")
print("=" * 80)

for eid in sorted(runtime.interfaces.keys()):

    print(eid)