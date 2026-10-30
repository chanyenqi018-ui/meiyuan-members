#!/usr/bin/env python3
"""Add a member.  Usage: add_member.py <id> "<name>" <600|1000> [issue-date YYYY-MM-DD]"""
import sys
from datetime import date
from store import *

a = sys.argv[1:]
if len(a) not in (3, 4):
    die('usage: add_member.py <id> "<name>" <600|1000> [issue-date]')
mid, name, t = a[0].strip().upper(), a[1].strip(), a[2]
tier = f"Gold {t}"
if tier not in TIERS:
    die("tier must be 600 or 1000")
issued = check_date(a[3]) if len(a) == 4 else date.today().isoformat()
y, mo, d = map(int, issued.split("-"))
try:
    exp = date(y + 2, mo, d)
except ValueError:  # 29 Feb
    exp = date(y + 2, mo, 28)
data = load()
if any(x["id"] == mid for x in data["members"]):
    die(f"{mid} already exists")
paid, credit = TIERS[tier]
data["members"].append({"id": mid, "name": name, "tier": tier, "paid": paid, "credit": credit,
                        "issued": issued, "expires": exp.isoformat(), "visits": []})
save(data)
print(f"OK added {mid} {name}, {tier}, credit RM{credit}, valid {issued} to {exp.isoformat()}")
print(f"Link: index.html?m={mid}")
