---
name: google-search
description: Google search functionality using Bright Data SERP API. Use when the user asks to search the web, perform online research, look up information online, find current information, or get search results. Supports single and batch search with configurable country, language, and result count.
---

# Google Search with Bright Data SERP API

## Getting Bright Data Credentials

### Step 1: Create a Bright Data Account

1. Go to [Bright Data](https://brightdata.com/)
2. Click "Start Free Trial" or "Sign Up"
3. Complete registration (they offer a free tier with trial credits)

### Step 2: Get Your API Token

1. Log in to [Bright Data Dashboard](https://brightdata.com/cp/api_tokens)
2. Navigate to **API Tokens** (or go to Settings > API Tokens)
3. Click **"Add new token"** if needed
4. Copy your token (format: `abc123def456...`)

> **Note:** The token looks like a long alphanumeric string. Keep it secure - it provides access to your Bright Data account.

### Step 3: Configure the Skill

Option A - Config file (recommended):
```bash
# Run setup first
python scripts/setup.py

# Edit the config file
open ~/.claude/google-search/config.json

# Replace empty string with your token:
{
  "api_key": "your-bright-data-token-here"
}
```

Option B - Environment variable:
```bash
export BRIGHTDATA_SERP_API_KEY="your-bright-data-token-here"
```

### Step 4: Verify Setup

```bash
python scripts/search.py "test search" "US" "en" "5"
```

Expected output with valid credentials:
```json
{
  "success": true,
  "query": "test search",
  "count": 5,
  "results": [...]
}
```

If you see `"success": false` with an API key error, double-check your token.

---

## Quick Start

> **First time?** Follow the [Getting Bright Data Credentials](#getting-bright-data-credentials) guide above.

1. Run setup to install SDK and create config:
   ```bash
   python scripts/setup.py
   ```

2. Add your API key to the config file:
   ```bash
   # Edit ~/.claude/google-search/config.json and add your key:
   {
     "api_key": "your-api-key-here"
   }
   ```

3. Use the search script:
   ```bash
   python scripts/search.py <query> [country] [language] [num_results]
   ```

## Usage Patterns

### Single Search
```bash
python scripts/search.py "Gausium Deutschland" "DE" "de" "10"
```

### Batch Search
```bash
python scripts/search.py --batch '["Gausium Deutschland", "Reinigungsroboter Händler Deutschland"]' "DE" "de" "10"
```

## Parameters

- `query`: Search query string (required)
- `country`: 2-letter country code (default: "US")
- `language`: Language code (default: "en")
- `num_results`: Number of results (default: 20)

## API Key Configuration

The search script looks for the API key in this order:

1. `BRIGHTDATA_SERP_API_KEY` environment variable (optional override)
2. `~/.claude/google-search/config.json` file (recommended)

## Response Format

Results are returned as JSON:
```json
{
  "success": true,
  "query": "...",
  "country": "US",
  "language": "en",
  "count": 10,
  "results": [
    {"title": "...", "url": "...", "snippet": "..."}
  ]
}
```

## Locale Detection

When users don't specify country/language, use context clues:
- US English domains (.com) → "US" "en"
- EU content → appropriate country code
- Non-English queries → detect language, default to US or likely origin

For detailed API documentation and country codes, see [references/api.md](references/api.md).

## Distributor Research Integration

When used with distributor-inspector skill:

### Search Patterns for Distributor Discovery
```bash
# By country and language
python scripts/search.py "Reinigungsroboter Händler" "DE" "de" "20"
python scripts/search.py "robot nettoyage distributeur" "FR" "fr" "20"
python scripts/search.py "limpiadora robot distribuidor" "ES" "es" "20"

# By competitor (competitive conversion)
python scripts/search.py "Pudu distributor" "DE" "en" "20"
python scripts/search.py "Gausium partner" "FR" "en" "20"
```

After search, use distributor-inspector to evaluate found URLs.
