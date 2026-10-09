# Publishing the firmbase plugin

## Release

1. Bump `version` in `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` (same value).
2. Merge to `main`. The `build` workflow validates both manifests and, when that version has no release yet, tags it `vX.Y.Z` and attaches two zips to a new GitHub release:
   - `firmbase-claude-<version>.zip`: Claude (upload to an organization or Cowork)
   - `firmbase-openai-<version>.zip`: ChatGPT and Codex (upload to platform.openai.com/plugins)

Locally: `python3 scripts/build.py` writes the same zips to `dist/`; `python3 scripts/build.py --check` only validates.

## Claude

Two separate listings, both from the developer portal at https://claude.ai/directory/manage (paid plan, GitHub connected with push access to this repository):

1. **MCP connector**: *Submit new* > *MCP connector* with `https://api.firmbase.be/mcp`. Needs a reviewer test account, at least three example prompts, and the privacy policy.
2. **Plugin bundle**: *Submit new* > *Plugin bundle*, repository `firmbase-be/firmbase-plugin`, branch `main`. Validate, answer the data handling questions, keep the GitHub push webhook. New versions are picked up from `main` automatically; no zip needed.

Claude Code users can already install from this repository (see README) without any listing.

## ChatGPT and Codex

One listing serves both, from https://platform.openai.com/plugins (organization owner, or a member with *Apps Management Write*; the organization must be verified as business so it publishes as firmbase).

1. Upload `firmbase-openai-<version>.zip`.
2. Connect the MCP server `https://api.firmbase.be/mcp` (OAuth; discovery and dynamic client registration are automatic).
3. Domain verification: copy the token from the dashboard into `KBO_OPENAI_APPS_CHALLENGE` on the kbo-server deployment, then check that `https://api.firmbase.be/.well-known/openai-apps-challenge` returns only the token as plain text.
4. Fill in a justification for each tool's annotations (all tools are read-only, non-destructive).
5. Review information: the test cases below, a video walkthrough URL that runs through all of them, release notes, and reviewer credentials.
6. Submit for review, then *Publish plugin* after approval.

MCP tool changes on the server are rescanned daily and go live without a new zip; manifest or skill changes need a new zip with a higher version.

### Reviewer account

A dedicated account (not a real user) with a reports subscription and Premium so every tool works, signing in with e-mail and password. No MFA, e-mail codes or magic links.

### Positive test cases

| Prompt | Expected tools | Expected result |
|---|---|---|
| What is the status and address of BE 0403.199.702? | lookup_vat or get_company | Name, legal form, active status and registered address of the company |
| Show the revenue and staff of Colruyt over the last three years | search_companies, get_financial_summary | Per-year revenue, profit and FTE from the filed annual accounts |
| Run a due-diligence check on BE 0403.199.702 before we extend credit | get_company, get_health_score, get_insolvency, check_withholding, screen_sanctions | Structured report with status, figures, health score, insolvency, 30bis/30ter and sanctions result |
| Which IT companies in Ghent have the highest revenue? | rank_companies, sector_statistics | Ranked list of companies with revenue, next to the sector median |
| In which companies does Jan Peeters hold a mandate? | find_person_mandates | List of companies with the role and start date of each mandate |

### Negative test cases

| Prompt | Why the plugin should not act |
|---|---|
| Change the registered address of my company in the KBO | All tools are read-only; firmbase cannot file changes with the register |
| Send an e-mail to the managing director of Colruyt | The plugin has no tools to send messages or contact people |
| Look up the annual accounts of Apple Inc. in the US | firmbase only covers Belgian companies |
