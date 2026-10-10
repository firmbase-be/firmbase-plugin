---
name: sales-workspace
description: Work in the user's own firmbase account - sales lists and their pipeline, notes and reminders, saved searches, the watchlist and watch rules, leads from the sales profile, and prospect exports. Use when the user asks to put companies on a list, move a company to contacted or won, add a note or a reminder, follow a company, save a search, decide on leads, or export a prospect list. Every change needs the user's confirmation in firmbase.
---

# The firmbase sales workspace

Besides the public company data, the firmbase MCP server reaches the user's own account: the lists their team works through, the notes and tasks on companies, what they follow, and the leads their sales profile proposes. On a team plan these are shared with the team.

## Reading is immediate

| Question | Tool |
|---|---|
| Which lists are there, how many companies in each status | `list_lists` |
| The companies on a list, their status and owner | `get_list` |
| Everything the account has on one company: lists, notes, followed | `get_company_workspace` |
| Open reminders, overdue first | `list_tasks` |
| Who a row or a reminder can be assigned to | `list_team_members` |
| Saved searches and their new matches | `list_saved_searches`, `get_saved_search_matches` |
| Followed companies, watch rules, the inbox | `list_watchlist`, `list_watch_rules`, `list_notifications` |
| The sales profile and the leads it proposed | `get_sales_profile`, `list_leads` |
| Earlier exports and rows left this month | `list_exports` |

## Changing anything needs the user

No write tool changes anything by itself. `create_list`, `add_to_list`, `fill_list_from_filter`, `update_list_items`, `add_note`, `watch_companies`, `create_watch_rule`, `decide_lead`, `export_prospects` and the other write tools validate the request and file it. The answer holds a `confirm_url` and an `action_id`.

1. Read first, so the request names the right list, note or lead (ids come from the read tools).
2. Call the write tool. When it answers `awaiting_confirmation`, give the user the `confirm_url` in one sentence that says what will happen. They confirm or reject it on the Approvals page in firmbase, where they see the companies by name.
3. Never say the change was made. When the user says they confirmed, or before you build on it (adding companies to a list you just asked to create), call `get_action_status`. Only `confirmed` means it was done; its `result` then holds what was made, such as the new `list_id`.
4. A request expires after a day. `rejected` means the user said no: don't file it again unless they ask.

Batch where you can. One `create_list` with all the numbers, or one `fill_list_from_filter`, is one confirmation for the user. Twenty `add_to_list` calls would be twenty.

## Plans

The lists, notes, tasks, watchlist and rules need a firmbase platform plan (Start, Team or Premium). Prospecting filters, saved searches, the sales profile and exports need Premium. A tool the plan does not include says so. Pass that on and point to https://firmbase.be/en/pricing.
