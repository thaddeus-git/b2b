# B2B Distributor Skills

Agent skills for B2B distributor inspection and qualification for **OrionStar Robotics** (cleaning robots).

These skills follow the [Agent Skills specification](https://agentskills.io/specification) and are compatible with Claude Code and Codex CLI.

## Installation

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

| Skill | Description |
|-------|-------------|
| [distributor-inspector](skills/distributor-inspector) | Inspect and score potential distributor websites against ICP criteria, categorize by niche market, and route to appropriate sales action. Includes built-in search script for LinkedIn lookup via Bright Data SERP API. |

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

## License

MIT
