"""Shared helpers for members.json (kept one-visit-per-line so it is easy to edit by hand)."""
import json, os, re, sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, "members.json")
TIERS = {"Gold 600": (600, 620), "Gold 1000": (1000, 1040)}  # tier: (paid, credit)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def die(msg):
    sys.exit("ERROR: " + msg)


def check_date(s):
    if not DATE_RE.match(s):
        die(f"date '{s}' must look like 2026-11-02 (YYYY-MM-DD)")
    try:
        date.fromisoformat(s)
    except ValueError:
        die(f"'{s}' is not a real date")
    return s


def load():
    with open(PATH, encoding="utf-8") as f:
        return json.load(f)


def j(v):
    return json.dumps(v, ensure_ascii=False)


def save(data):
    out = ['{', '  "members": [']
    ms = data["members"]
    for i, m in enumerate(ms):
        out.append('    {')
        for k in ("id", "tier", "paid", "credit", "issued", "expires"):
            out.append(f'      "{k}": {j(m[k])},')
        if m.get("receipt"):
            out.append(f'      "receipt": {j(m["receipt"])},')
        out.append('      "visits": [')
        vs = m["visits"]
        for n, v in enumerate(vs):
            line = f'        {{"date": {j(v["date"])}, "service": {j(v["service"])}, "amount": {j(v["amount"])}}}'
            out.append(line + ("," if n < len(vs) - 1 else ""))
        out.append('      ]')
        out.append('    }' + ("," if i < len(ms) - 1 else ""))
    out += ['  ]', '}']
    text = "\n".join(out) + "\n"
    json.loads(text)  # must stay valid
    with open(PATH, "w", encoding="utf-8") as f:
        f.write(text)


def balance(m):
    return m["credit"] - sum(v["amount"] for v in m["visits"])


def parse_amount(s):
    try:
        a = float(s)
    except ValueError:
        die(f"amount '{s}' is not a number")
    if a <= 0:
        die("amount must be more than 0")
    return int(a) if a == int(a) else round(a, 2)
