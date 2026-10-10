# firmbase plugin for Claude and Codex

Belgian company data inside your AI assistant, from the official sources: the Crossroads Bank for Enterprises (KBO/BCE/CBE) register, the annual accounts filed with the National Bank of Belgium, and the Belgian Official Gazette. Refreshed every night.

The plugin connects the [firmbase MCP server](https://firmbase.be/en/api/mcp) and adds four skills:

- **belgian-company-data**: which of the 32 data tools answers which question, how to identify a company, and how to cite the sources.
- **company-due-diligence**: a structured check of a counterparty, from status and figures to insolvency notices, the 30bis/30ter withholding obligation and sanctions screening.
- **prospect-list**: target companies in a sector and region, ranked on revenue or staff, next to the sector median, and saved as a list in firmbase if you want.
- **sales-workspace**: your own firmbase account through 34 more tools: sales lists and their pipeline, notes and reminders, saved searches, the watchlist and watch rules, leads and exports.

## Nothing changes without you

The data tools only read. The workspace tools read your lists, notes and watchlist directly, but they never change them on their own. When the assistant wants to change something, such as creating a list, moving a company to *won*, adding a note or following a company, it files a request. You see that request on the **Approvals** page in firmbase, with the companies by name, and you confirm or reject it there. Nothing happens until you click **Confirm**, and a request expires after a day.

## Install

### Claude Code

```bash
claude plugin marketplace add firmbase-be/firmbase-plugin
claude plugin install firmbase@firmbase
```

Then run `/mcp` in Claude Code, choose **firmbase** and **Authenticate**. Your browser opens firmbase to sign in.

### Codex

```bash
codex plugin marketplace add firmbase-be/firmbase-plugin
codex plugin add firmbase@firmbase
```

Codex asks you to sign in with firmbase when the plugin is installed.

### Claude.ai, ChatGPT and other MCP clients

No plugin needed. Add `https://api.firmbase.be/mcp` as a custom connector and sign in when asked. See [firmbase.be/en/api/mcp](https://firmbase.be/en/api/mcp) for per-client steps.

## Sign-in and pricing

You sign in with your firmbase account through OAuth. You don't paste an API key anywhere. The connection gets its own key on your account, named after the client, so you can see its usage and revoke it in the [dashboard](https://firmbase.be/en/dashboard).

Each tool call is one call on your firmbase plan. The register tools work on the free plan (100 calls a day). Annual accounts, people and rankings need Pro or a reports subscription; the health score and the full report need a reports subscription; sanctions screening needs Premium. The workspace tools need a firmbase platform plan (Start, Team or Premium); prospecting filters, saved searches, the sales profile and exports need Premium. See [pricing](https://firmbase.be/en/pricing).

## Privacy

firmbase receives the tool calls your assistant makes, such as a company number or a search term, the same as an API call. It never sees the conversation itself. See the [privacy policy](https://firmbase.be/en/privacy).

## Support

Open an issue in this repository, or write to support@firmbase.be.
