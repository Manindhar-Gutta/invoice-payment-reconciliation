# Invoice ↔ Payment Reconciliation (Python)

**Before:** someone opens the invoice list and the bank export every week, VLOOKUPs messy payment references, and colour-codes what doesn't match. About 2 hours, and it's easy to get wrong.

**After:** one command creates a 5-tab Excel report in seconds.

| Tab | What it shows |
|---|---|
| Summary | row count per check |
| Matched | invoice paid in full (±0.01) |
| Amount mismatch | paid, but short or over, with the difference |
| Unpaid invoices | no payment found |
| Unmatched payments | cash with no invoice reference, for follow-up |

## Run it
```bash
pip install pandas openpyxl
python make_data.py                      # creates sample invoices.xlsx + payments.csv
python reconcile.py invoices.xlsx payments.csv recon_report.xlsx
python test_reconcile.py
```

## How it works
1. Pulls the invoice number out of free-text bank references (`"Payment inv-1003"` → `INV-1003`).
2. Outer-joins invoices to payments, so nothing drops out silently.
3. Sorts every row into one of four buckets. Every invoice and every payment lands in exactly one.
4. Stops with a plain message if an input column is missing.

The same logic maps one-to-one to Alteryx (RegEx → Join → Formula → Filter → Output) or KNIME (String Manipulation → Joiner → Math Formula → Row Splitter → Excel Writer).

*All data is synthetic.*
