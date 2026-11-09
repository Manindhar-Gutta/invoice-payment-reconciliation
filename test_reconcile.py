import pandas as pd
from reconcile import reconcile


def test_buckets():
    inv = pd.DataFrame({"invoice_no": ["INV-1", "INV-2", "INV-3"], "amount": [100.0, 200.0, 300.0]})
    pay = pd.DataFrame({"reference": ["pay inv-1", "INV-2 part", "no ref"], "amount": [100.0, 150.0, 50.0]})
    t = reconcile(inv, pay)
    assert list(t["Matched"]["invoice_no"]) == ["INV-1"]
    assert list(t["Amount mismatch"]["difference"]) == [-50.0]
    assert list(t["Unpaid invoices"]["invoice_no"]) == ["INV-3"]
    assert len(t["Unmatched payments"]) == 1


if __name__ == "__main__":
    test_buckets(); print("ok")
