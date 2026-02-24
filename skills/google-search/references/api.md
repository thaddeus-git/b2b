# Bright Data SERP API Reference

## Setup

Install the SDK:
```bash
pip install brightdata-sdk
```

Set your API key as environment variable:
```bash
export BRIGHTDATA_SERP_API_KEY="your-api-key-here"
```

## Search Script Usage

### Single Search
```bash
python scripts/search.py <query> [country] [language] [num_results]
```

**Parameters:**
- `query` (required): Search query string
- `country` (optional): 2-letter country code (default: "US")
- `language` (optional): Language code (default: "en")
- `num_results` (optional): Number of results (default: 20)

**Examples:**
```bash
python scripts/search.py "best restaurants" "US" "en" "10"
python scripts/search.py "meilleur restaurant" "FR" "fr" "15"
python scripts/search.py "beste restaurants" "DE" "de" "20"
```

### Batch Search
```bash
python scripts/search.py --batch <queries_json> [country] [language] [num_results]
```

**Example:**
```bash
python scripts/search.py --batch '["pizza", "sushi", "tacos"]' "US" "en" "10"
```

## Response Format

### Success Response
```json
{
  "success": true,
  "query": "best restaurants",
  "country": "US",
  "language": "en",
  "count": 10,
  "results": [
    {
      "title": "Title of result",
      "url": "https://example.com",
      "snippet": "Description of result..."
    }
  ]
}
```

### Error Response
```json
{
  "error": "Error message",
  "success": false,
  "query": "search query"
}
```

## Supported Country Codes

Common country codes:
- US: United States
- GB: United Kingdom
- DE: Germany
- FR: France
- ES: Spain
- IT: Italy
- CA: Canada
- AU: Australia
- JP: Japan
- KR: South Korea
- CN: China
- IN: India
- BR: Brazil
- MX: Mexico
- NL: Netherlands
- BE: Belgium
- CH: Switzerland
- PL: Poland
- CZ: Czech Republic
- SE: Sweden
- NO: Norway
- DK: Denmark
- FI: Finland
- GR: Greece
- PT: Portugal
- IE: Ireland
- NZ: New Zealand
- SG: Singapore
- MY: Malaysia
- TH: Thailand
- VN: Vietnam
- ID: Indonesia
- PH: Philippines
- HK: Hong Kong
- TW: Taiwan
- AE: United Arab Emirates
- SA: Saudi Arabia
- IL: Israel
- TR: Turkey
- AR: Argentina
- CL: Chile
- CO: Colombia
- PE: Peru
- EG: Egypt
- NG: Nigeria
- KE: Kenya
- ZA: South Africa
