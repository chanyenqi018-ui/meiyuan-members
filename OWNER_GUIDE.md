# Owner guide (Chris)

All member data lives in one file: **members.json**. Customers can only view their own card. They cannot change anything. Only you can edit the file.

Each member's link: `https://<your-site>/index.html?m=MY-G5833` (change the member number).

## Edit on your phone (GitHub)
1. Open the repo in GitHub, tap **members.json**, tap the pencil (Edit).
2. Make the change below. Keep every comma, quote and bracket.
3. Tap **Commit changes**. The site updates in about 1 minute.

## Add a visit
Find the member. Under `"visits": [` add **one line per visit**:

```
{"date": "2026-11-02", "service": "Gel manicure", "amount": 80}
```

- Date is `YYYY-MM-DD`. Amount is a number, no "RM".
- A **comma at the end of every line except the last one**.
- Balance = credit minus all visit amounts. The page works it out.

Example with two visits:
```
"visits": [
  {"date": "2026-11-02", "service": "Gel manicure", "amount": 80},
  {"date": "2026-11-20", "service": "Foot reflexology", "amount": 120}
]
```

## Add a member
Copy a whole member block (from `{` to `}`), paste it after the last member, and put a comma between the two blocks. Change:
- `id` (e.g. MY-G5083), `name`, `issued`, `expires` (2 years later)
- Gold 600: `"tier": "Gold 600", "paid": 600, "credit": 620`
- Gold 1000: `"tier": "Gold 1000", "paid": 1000, "credit": 1040`
- `"visits": []` (empty for a new member)

## Fix a wrong entry
Edit that visit's line (date, service or amount), or delete the whole line. If you delete the last line, remove the comma on the line above it.

## If the page says "Can't read member data"
There is a typo (usually a missing or extra comma, or a missing quote). Open the edit again and check the line you changed. Or use GitHub's "Revert" on your last commit.

## Using the bot or scripts instead
```
python3 add_member.py MY-G5083 "Amy Tan" 600 2026-11-05
python3 add_visit.py MY-G5083 2026-11-10 "Gel manicure" 80
```
Both keep the one-visit-per-line format.

## Privacy
Once on GitHub Pages, `members.json` is public to anyone who knows the address. Only keep name, dates, services and amounts there. No phone, IC or payment details.

## Receipts
Put the member's receipt PDF in the `receipts/` folder (for example `receipts/MY-G5833.pdf`), then add one line to that member's block in members.json:
```
"receipt": "receipts/MY-G5833.pdf",
```
The member page then shows a **View receipt** button. If the line is missing, or the file is not in the folder, no button shows.
