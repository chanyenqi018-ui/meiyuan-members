#!/usr/bin/env python3
"""Record a visit.   Usage: add_visit.py <id> <date YYYY-MM-DD> "<service>" <amount> [--force]"""
import sys
from store import *

args = [a for a in sys.argv[1:] if a != "--force"]
force = "--force" in sys.argv
if len(args) != 4:
    die('usage: add_visit.py <id> <date YYYY-MM-DD> "<service>" <amount> [--force]')
mid, d, service, amt = args
mid = mid.strip().upper(); check_date(d); amt = parse_amount(amt)
data = load()
m = next((x for x in data["members"] if x["id"] == mid), None)
if not m:
    die(f"no member {mid}")
if d > m["expires"]:
    print(f"WARNING: card expired on {m['expires']}")
    if not force: die("add --force to record anyway")
left = balance(m) - amt
if left < 0 and not force:
    die(f"only RM{balance(m)} left, visit is RM{amt}. Add --force to record anyway")
m["visits"].append({"date": d, "service": service.strip(), "amount": amt})
m["visits"].sort(key=lambda v: v["date"])
save(data)
print(f"OK {mid} {m['name']}: {d} {service} RM{amt}. Balance left: RM{left}")
