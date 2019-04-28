import json
from redis import Redis, ConnectionPool

pool = ConnectionPool()
r = Redis(connection_pool=pool)

members = r.smembers("jufaanli:case")
case_numbers = set()

for each in members:
    item = json.loads(each)
    case_number = item.get("case_no", None)
    if case_number:
        case_numbers.add(case_number)

with open("case_number.dat", mode="w", encoding="utf-8") as f:
    for each in case_numbers:
        f.write(each+"\n")

