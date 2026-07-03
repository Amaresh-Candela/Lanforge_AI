from tools.inventory import Inventory

inventory = Inventory(

    host="192.168.207.78"

)

print("\nEthernet Ports\n")

for port in inventory.get_eth_ports():

    print(port)

print("\nStations\n")

for sta in inventory.get_stations():

    print(sta)

print("\nRadios\n")

for radio in inventory.get_radios():

    print(radio)

print("\nAll Ports\n")

for port in inventory.get_all_ports():

    print(port)