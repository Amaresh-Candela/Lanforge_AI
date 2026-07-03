from tools.inventory import Inventory
from agent.inventory_resolver import InventoryResolver

inventory = Inventory(

    host="192.168.207.78"

)

resolver = InventoryResolver(inventory)

required = [

    "station",

    "upstream",

    "radio"

]

result = resolver.resolve(required)

print()

print(result)