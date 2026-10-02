---
name: company-due-diligence
description: Run a structured due-diligence or credit check on a Belgian company with firmbase - before signing a contract, onboarding a supplier or customer (KYC/KYB), or extending credit. Use when the user asks to check, vet, screen or assess a Belgian company or counterparty.
---

# Due diligence on a Belgian company

Work through the steps in order. Every step uses a firmbase tool; see the `belgian-company-data` skill for the tool map.

1. **Identify** the company with `search_companies` or `lookup_vat`, and confirm the enterprise number with the user if the match is not certain.
2. **Identity and status** with `get_company`: legal form, start date, registered address, main activity, and the legal situation. Anything other than normal (stopped, in liquidation, bankrupt) is the headline.
3. **Figures** with `get_financial_summary`: revenue or gross margin, net result, equity, solvency and liquidity over the last years. Describe the trend, not just the latest year.
4. **Health score and credit limit** with `get_health_score`, including the reasons it gives.
5. **People** with `get_officers`, plus recent board changes from `get_publications`. With `get_board_network`, look for directors linked to companies that went bankrupt.
6. **Red flags**: `get_insolvency` for court notices, `check_withholding` for the 30bis/30ter obligation, `screen_sanctions` for the company, its board and its shareholders.
7. **Verdict**: a short paragraph, then the three points a credit controller should look at, each one tied to the data that raised it.

When a step is not on the user's plan, say so in that section and carry on with the rest.

Mark which statements come from the register or the filed accounts, and which from firmbase's models (the health score and the credit limit). End with a link to the full report: `https://firmbase.be/en/company/<number>/<name>` (ten digits, the name lowercased with hyphens).
