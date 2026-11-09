"""Match bank payments to invoices and write a 4-tab Excel report.

Usage: python reconcile.py invoices.xlsx payments.csv recon_report.xlsx
"""
import sys
import pandas as pd

TOLERANCE = 0.01  # rounding allowed between invoice and payment


def reconcile(inv: pd.DataFrame, pay: pd.DataFrame) -> dict:
    for name, df, cols in [("invoices", inv, {"invoice_no", "amount"}),
                           ("payments", pay, {"reference", "amount"})]:
        missing = cols - set(df.columns)
        if missing:
            raise SystemExit(f"{name} file is missing column(s): {', '.join(sorted(missing))}")
    pay = pay.copy()
    # Pull the invoice number out of free-text bank references, e.g. "Payment inv-1003".
    pay["invoice_no"] = pay["reference"].str.upper().str.extract(r"(INV-\d+)", expand=False)
    m = inv.merge(pay, on="invoice_no", how="outer", suffixes=("_inv", "_pay"), indicator=True)
    both = m[m["_merge"] == "both"].copy()
    both["difference"] = (both["amount_pay"] - both["amount_inv"]).round(2)
    ok = both["difference"].abs() <= TOLERANCE
    return {
        "Matched": both[ok],
        "Amount mismatch": both[~ok],
        "Unpaid invoices": m[m["_merge"] == "left_only"],
        "Unmatched payments": m[m["_merge"] == "right_only"],
    }


def main(inv_path, pay_path, out_path):
    tabs = reconcile(pd.read_excel(inv_path), pd.read_csv(pay_path))
    with pd.ExcelWriter(out_path) as xw:
        summary = pd.DataFrame({"Check": list(tabs), "Rows": [len(t) for t in tabs.values()]})
        summary.to_excel(xw, sheet_name="Summary", index=False)
        for name, df in tabs.items():
            df.drop(columns="_merge").to_excel(xw, sheet_name=name, index=False)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)
    main(*sys.argv[1:])
