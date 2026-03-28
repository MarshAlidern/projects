import re
import json

with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

lines = text.splitlines()

items = []
prices = []
product_names = []

i = 0
while i < len(lines):
    line = lines[i].strip()

    if re.match(r"^\d+\.", line):
        name = line.split(".", 1)[1].strip()

        if i + 1 < len(lines) and "x" not in lines[i + 1]:
            name += " " + lines[i + 1].strip()
            i += 1

        qty_line = lines[i + 1].strip()
        total_line = lines[i + 2].strip()

        qty_price_match = re.search(r"([\d,]+)\s*x\s*([\d\s,]+)", qty_line)
        if qty_price_match:
            qty = float(qty_price_match.group(1).replace(",", "."))
            unit_price = float(qty_price_match.group(2).replace(" ", "").replace(",", "."))

        total = float(total_line.replace(" ", "").replace(",", "."))

        items.append({
            "name": name,
            "quantity": qty,
            "unit_price": unit_price,
            "total": total
        })

        product_names.append(name)
        prices.append(total)

        i += 3
    else:
        i += 1


date_time_match = re.search(r"Время:\s*([\d\.]+\s[\d:]+)", text)
date_time = date_time_match.group(1) if date_time_match else None

payment_match = re.search(r"(Банковская карта|Наличные)", text)
payment_method = payment_match.group(1) if payment_match else None

total_match = re.search(r"ИТОГО:\s*([\d\s,]+)", text)
total_amount = float(total_match.group(1).replace(" ", "").replace(",", ".")) if total_match else sum(prices)

output = {
    "date_time": date_time,
    "payment_method": payment_method,
    "items": items,
    "product_names": product_names,
    "prices": prices,
    "total_amount": total_amount
}

print(json.dumps(output, ensure_ascii=False, indent=4))
