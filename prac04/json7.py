import json
with open("sample-data.json", "r") as f:
    data = json.load(f)

print("Interface Status")
print("=" * 80)
print(f"{'DN':<50} {'Description':<20} {'Speed':<7} {'MTU':<6}")
print("-" * 80)
for i in data["imdata"]:
    a = i["l1PhysIf"]["attributes"]

    dn = a.get("dn", "")
    descr = a.get("descr", "")
    speed = a.get("speed", "")
    mtu = a.get("mtu", "")

    print(f"{dn:<50} {descr:<20} {speed:<7} {mtu:<6}")