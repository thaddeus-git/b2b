---
name: google-search
description: Google search functionality using Bright Data SERP API. Use when the user asks to search the web, perform online research, look up information online, find current information, or get search results. Supports single and batch search with configurable country, language, and result count.
---

# Google Search with Bright Data SERP API

## Quick Start

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
