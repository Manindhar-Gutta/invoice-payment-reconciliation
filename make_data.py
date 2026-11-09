"""Make synthetic invoices.xlsx and payments.csv (fake companies, fake amounts)."""
import random
import pandas as pd

random.seed(7)
customers = ["Acme Traders", "Blue Fern Ltd", "Corvid Foods", "Delta Parts", "Ember Retail"]
inv = pd.DataFrame({
    "invoice_no": [f"INV-{1000 + i}" for i in range(40)],
    "customer": [random.choice(customers) for _ in range(40)],
    "amount": [round(random.uniform(200, 5000), 2) for _ in range(40)],
    "due_date": pd.date_range("2026-10-01", periods=40, freq="D").date,
})
pay = inv.sample(frac=0.85, random_state=7)[["invoice_no", "customer", "amount"]].copy()
pay["reference"] = "Payment " + pay["invoice_no"].str.lower()   # messy bank text
pay.loc[pay.index[:3], "amount"] -= 50                           # short-paid
pay = pay.drop(columns="invoice_no")
pay = pd.concat([pay, pd.DataFrame({"customer": ["Unknown"], "amount": [999.0],
                                    "reference": ["Transfer no ref"]})])  # unmatched cash
inv.to_excel("invoices.xlsx", index=False)
pay.sample(frac=1, random_state=1).to_csv("payments.csv", index=False)
print(len(inv), "invoices,", len(pay), "payments")
