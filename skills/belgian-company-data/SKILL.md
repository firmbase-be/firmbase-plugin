---
name: belgian-company-data
description: Look up Belgian companies with the firmbase tools - identity, status, addresses, activities, directors, shareholders, annual accounts, Official Gazette publications, insolvency notices, withholding obligations and sanctions. Use whenever a question names a Belgian company, an enterprise number (0123.456.789), a Belgian VAT number (BE0123456789), a director, or asks about Belgian companies in a sector or municipality.
---

# Belgian company data with firmbase

The firmbase MCP server answers from the official sources: the Crossroads Bank for Enterprises (KBO/BCE/CBE) register, the annual accounts filed with the National Bank of Belgium (NBB), and the Belgian Official Gazette (Belgisch Staatsblad / Moniteur belge). The data is refreshed every night.

## Identify the company first

Every other tool takes the 10-digit enterprise number (`0403.199.702` or `0403199702`). A Belgian VAT number is `BE` plus the same ten digits.

- Only a name: `search_companies` (filter on postcode, municipality, NACE activity or legal form when the name is common).
- A VAT number: `lookup_vat`. Any EU VAT number: `validate_eu_vat` (VIES).
- A number that may be an establishment unit (starts with 2): `get_entity`.

Don't guess a number. When a search gives several candidates, say which one you picked and why.

## Which tool answers what

| Question | Tool |
|---|---|
| Register record: name, status, legal form, address, activities | `get_company` |
| Branches and establishment units | `get_establishments` |
| Former names, addresses, legal forms | `get_company_history` |
| Official Gazette publications (statutes, board changes) | `get_publications` |
| Who is registered at an address | `search_addresses` |
| What a NACE code means | `get_nace_code` |
| Key figures and ratios per book year | `get_financial_summary` |
| Every filed annual account, or every rubric of one | `list_annual_reports`, `get_annual_report_financials` |
| Directors, managers, auditors | `get_officers` |
| Every mandate of one person | `find_person_mandates` |
| Shareholders, participations, board network | `get_shareholders`, `get_participations`, `get_board_network` |
| Companies sharing a phone number, e-mail or website | `lookup_contact` |
| Health score and credit limit, with the reasons | `get_health_score` |
| The whole report in one call | `get_company_report` |
| 30bis/30ter withholding obligation | `check_withholding` |
| Bankruptcy and reorganisation notices | `get_insolvency`, `list_insolvency_notices` |
| Sanctions screening of the company, board and shareholders | `screen_sanctions` |
| Rank companies on a metric, sector benchmarks | `rank_companies`, `sector_statistics` |
| How many companies a ranking filter holds | `count_companies` |
| Count companies per sector, municipality or year | `aggregate_companies` |
| Up to 100 companies at once, e.g. names for a list of numbers | `get_companies_batch` |
| What changed at a company, newest first | `get_company_changes` |
| How fresh the data is | `dataset_info` |

Prefer the narrow tool over `get_company_report` when one section answers the question: the full report is large.

The user's own lists, notes, watchlist and leads are in the workspace tools: see the **sales-workspace** skill.

## Plans

Each tool call is one call on the user's firmbase plan. The register tools work on the free plan. Annual accounts, people, insolvency notices and rankings need Pro or a reports subscription. The health score, the full report and the withholding check need a reports subscription, and sanctions screening needs Premium. The change history of a company needs a Business API plan. A tool the plan does not include returns an error that names what is required. Pass that on to the user instead of working around it, and point them to https://firmbase.be/en/pricing.

## How to answer

- Say where each statement comes from: the register, the filed accounts, the Gazette, or a firmbase model. The health score, the credit limit and the sector benchmarks are firmbase models built on those sources, not register data.
- Give amounts in euro with the book year they belong to. Accounts are filed months after a year closes, so the latest year may be missing.
- Link each company you name to its report: `https://firmbase.be/en/company/<number>/<name>`, with the number as ten digits without dots and the name lowercased with hyphens (`0403199702/bnp-paribas-fortis`). A slightly wrong name still lands on the right page; a link without the name does not.
