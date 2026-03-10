import re
with open("raw.txt", "r", encoding="utf-8") as f:
    data = f.read()
prices = re.findall(r"\b\d+(?:\s\d+)*,\d{2}\b", data)
products = re.findall(r"\d+\.\n.+", data)
stoimost = re.findall(r"Стоимость\s*\n(\d+(?:\s\d+)*,\d{2})", data)
nums = [float(x.replace(" ", "").replace(",", ".")) for x in stoimost]
total = sum(nums)
dateandtime = re.findall(r"\b(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})\b", data)
payment = re.findall(r"Банковская карта:", data)

print("All prices:")
for i in prices:
    print(i)
print("All products:")
for i in products:
    print(i)
print("Total:", total)
for date, time in dateandtime:
    print("Date and time:", date, time)
for i in payment:
    print("Payment method: ", i)

