---
name: prospect-list
description: Build a list of Belgian target companies in a sector and region, ranked on revenue or staff, with firmbase. Use when the user asks for prospects, leads, a target list, the largest companies in a sector, or competitors in a Belgian municipality or province.
---

# Prospect list of Belgian companies

1. **Sector to NACE code.** Translate the sector into one or more NACE-BEL codes. Check them with `get_nace_code`. A 2-digit code covers a whole division; a 5-digit code is a single activity.
2. **Region.** Use the municipality, postcode(s) or province the user gave. Without one, the list covers Belgium.
3. **Rank.** Call `rank_companies` for the codes and region, once with `metric` `revenue_base` and once with `employees_fte`. Merge the results into the 20 most relevant companies. `revenue_base` is revenue, or the gross margin where a company files abridged accounts and publishes no revenue; say which one a figure is.
4. **Context.** Use `sector_statistics` to give the sector median beside each company's figures, so the user can see who is above or below it.
5. **Present** a table with: name, enterprise number, municipality, revenue (or gross margin), staff, net result, book year, and a link `https://firmbase.be/en/company/<number>/<name>` (ten digits, the name lowercased with hyphens).

Rankings need a Pro plan or a reports subscription. If the tool answers that the plan does not include it, tell the user, and offer what the free register tools can still do: `search_companies` on activity and municipality, without the figures.
