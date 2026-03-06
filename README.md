# B2B Distributor Skills

Agent skills for B2B distributor inspection and qualification for **OrionStar Robotics** (cleaning robots).

These skills follow the [Agent Skills specification](https://agentskills.io/specification) and are compatible with Claude Code and Codex CLI.

## Quick Start

**Inspect a lead (recommended workflow):**

```bash
# Step 1: Classify
Use skill: lead-classifier
Input: https://company.com
Output: "Route to: ka-inspector"

# Step 2: Inspect
Use skill: ka-inspector
Input: https://company.com
Output: Full scored report

Total time: ~90 seconds (50% faster than trial-and-error)
```

## Installation

### Prerequisites

```bash
# Install Playwright CLI
npm install -g @playwright/cli@latest

# Install shared utilities
cd skills/shared-scripts
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"

# Configure Bright Data API key
# Create ~/.claude/config.json:
{
  "brightdata_api_key": "your-api-key-here"
}
```

### Marketplace (Claude Code)

```bash
/plugin marketplace add thaddeus-git/b2b
/plugin install b2b@b2b
```

### Manually

#### Claude Code

Copy the skill folder to your project's `/.claude` folder:

```bash
# Clone the repository
git clone -b inspection git@github.com:thaddeus-git/b2b.git

# Copy skills to your project
cp -r b2b/skills/* /path/to/your/project/.claude/skills/
```

Or copy to your global skills folder:

```bash
cp -r b2b/skills/distributor-inspector ~/.claude/skills/
cp -r b2b/scripts ~/.claude/skills/distributor-inspector/scripts/
```

#### Codex CLI

Copy to the Codex skills directory:

```bash
cp -r b2b/skills/distributor-inspector ~/.codex/skills/
```

## Skills

### lead-classifier (NEW in v2.0.0)

Quickly classify lead type and route to correct inspector.

- **Time:** 30 seconds
- **Output:** Routing recommendation (distributor/KA/channel-partner/exclude)
- **Efficiency:** 50% faster than trial-and-error

### distributor-inspector

Evaluate potential distributors for OrionStar cleaning robots.

- **Mode:** Standard (text-only) or Deep (with image analysis)
- **Output:** Scored report (0-100) with action recommendation

### ka-inspector

Evaluate potential KA end customers (companies that BUY and USE robots).

- **Mode:** Standard or Deep
- **Output:** Pilot-readiness assessment

### channel-partner-inspector

Evaluate potential channel partners (companies with client relationships).

- **Output:** Partnership recommendation

### lead-enricher

Enrich lead CSVs with website, LinkedIn, and company data.

- **Input:** CSV with names, companies, phones, emails
- **Output:** Enriched CSV with website, LinkedIn, verification status

## Usage

### Distributor Inspector

Use when evaluating websites as potential distributors for OrionStar Robotics:

```
Use the Skill tool with: distributor-inspector
Input: URL to inspect
Output: Markdown report with company profile, tags, score, and action recommendation
```

**Scoring System:**

| Component | Points |
|-----------|--------|
| Required: Sells as expected | PASS/FAIL |
| Bonus: Cleaning equipment | +30 to +90 |
| Bonus: Competitor footprint | +30 to +90 |
| Bonus: Channel capability | +0 to +20 |

> **Competitor distributors are TOP prospects** - they already have the infrastructure, training, and customer base.

**Actions returned:**
- `prioritize` (90+): High-potential distributor, contact first
- `standard` (70-89): Good fit, normal outreach
- `explore` (50-69): Potential but needs research
- `exclude` (<50): Does not meet criteria
- `route-to-sales` + `competitive-conversion`: Competitor distributor (Pudu, Gausium, etc.)

## Configuration

**Bright Data SERP API (required for LinkedIn lookup):**

```bash
# Run setup from the distributor-inspector skill directory
python3 scripts/setup.py

# Edit the config file and add your API key
open ~/.claude/distributor-inspector/config.json
```

**Reference files** (bundled with the skill):

| File | Purpose |
|------|---------|
| `references/keywords.md` | Product/service keywords by target industry |
| `references/tags.md` | Niche market tag taxonomy |
| `references/competing-brands.md` | Competitor brands to detect |

To customize, edit these files directly in your installed skill folder.

## ICP Criteria

The skill evaluates distributors against OrionStar Robotics' Ideal Customer Profile:

**Must-Have:**
- 20-500 employees, ~€10M revenue
- Complete teams (Sales, Deployment, After-sales)
- Quantifiable SLA capability
- Trial/PoC support capability
- Multi-city market coverage

**Bonus Criteria:**
- Distribution network (tier-2 resellers)
- System integration capability
- Property management/FM customers
- Local industry resources
- Competitor channel background (Pudu, Gausium)

## Target Industries

1. Commercial cleaning equipment distributors
2. Property management (FM/IFM)
3. Cleaning service contractors
4. System integrators
5. B2B-capable consumer electronics distributors

## Deep Mode (Image Analysis)

Both skills support an optional `mode="deep"` argument for enhanced analysis:

```bash
# Standard mode (default) - text-only, fast (~30 seconds)
distributor-inspector url="example.de"
ka-inspector url="example.com"

# Deep mode - includes image analysis (~90 seconds)
distributor-inspector url="example.de" mode="deep"
ka-inspector url="example.com" mode="deep"
```

**Deep mode adds:**
- **distributor-inspector:** Team photo analysis (employee count), competitor logo detection, certification badges
- **ka-inspector:** Facility photos, location count verification, partnership/certification detection

## What's New in v2.0.0

### Major Restructure
- **NEW:** lead-classifier skill for efficient routing (50% time savings)
- **CONSOLIDATED:** All ICP files moved to shared-references/
- **UNIFIED:** Single SERP search utility (serp_search.py)
- **SIMPLIFIED:** Single shared config at ~/.claude/config.json

### Migration Guide
- Old skill-specific configs still work (backward compatible)
- Update imports from `skills/shared/` to `skills/shared-scripts/`
- References updated to use `../shared-references/` paths

### Removed
- Duplicate ICP files (1,195 lines)
- distributor-inspector/scripts/ (consolidated to shared-scripts/)

## License

MIT
