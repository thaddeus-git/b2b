# crawl4ai Integration Design

**Date:** 2026-02-25
**Status:** Approved
**Author:** Claude + User collaboration

## Problem Statement

The `distributor-inspector` skill currently uses Chrome DevTools MCP for website inspection, which has three key limitations:

1. **Speed**: Sequential processing only - one URL at a time
2. **Cost**: Full accessibility tree parsing, no browser pooling
3. **Batch processing**: No native parallel URL processing

## Proposed Solution

Replace Chrome DevTools MCP with **crawl4ai API server** for website content extraction.

## Architecture

### Current Flow
```
URL → Chrome DevTools MCP (navigate_page, take_snapshot) → LLM parses accessibility tree → Score
```

### Proposed Flow
```
URL → crawl4ai API server → fit_markdown content → LLM extracts structured data → Score
```

### Infrastructure

| Component | Description |
|-----------|-------------|
| **crawl4ai Docker** | `unclecode/crawl4ai:latest` on port 11235 |
| **API endpoint** | `POST http://localhost:11235/crawl` |
| **Browser pooling** | crawl4ai manages browser instance reuse |
| **No MCP dependency** | Direct HTTP calls from SKILL.md |

## Content Extraction Strategy

### Mode: `fit_markdown` with `PruningContentFilter`

**Why fit_markdown:**
- Removes navigation, footers, ads, boilerplate
- Reduces token usage by 50-70%
- Preserves relevant content for distributor scoring

**Content needed for scoring:**
- Company name, products, services, brands
- Team/employee indicators
- Geographic coverage
- SLA/service mentions
- Competitor brand mentions (Pudu, Gausium, LionsBot, etc.)

**API payload:**
```json
{
  "urls": ["https://example.com"],
  "browser_config": {
    "type": "BrowserConfig",
    "params": {
      "headless": true,
      "viewport": {"width": 1200, "height": 800}
    }
  },
  "crawler_config": {
    "type": "CrawlerRunConfig",
    "params": {
      "markdown_generator": {
        "type": "DefaultMarkdownGenerator",
        "params": {
          "content_filter": {
            "type": "PruningContentFilter",
            "params": {"threshold": 0.6}
          }
        }
      },
      "page_timeout": 60000,
      "delay_before_return_html": 2.0
    }
  }
}
```

## Batch Processing

### Configuration

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| `max_concurrent` | 5-10 | Balance speed vs server load |
| `page_timeout` | 60s | Allow for slow sites |
| `delay_before_return_html` | 2s | JS rendering time |

### Batch Workflow

```
1. Input: List of URLs from google-search results
2. crawl4ai arun_many(): Process N URLs concurrently
3. Results: Array of {url, markdown, success, error}
4. LLM processing: Score each result independently
5. Output: Ranked distributor list with actions
```

### API Call (Batch)

```json
{
  "urls": ["https://url1.com", "https://url2.com", "https://url3.com"],
  "crawler_config": { ... }
}
```

Response includes array of results, one per URL.

## Error Handling: Fail Fast

| Error | Action |
|-------|--------|
| Docker not running | Error: "crawl4ai server not running. Start with: `docker run -d -p 11235:11235 unclecode/crawl4ai:latest`" |
| Page timeout | Return error with URL for manual review |
| Empty content | Return error with URL for manual review |
| Any crawl failure | Return error object, continue to next URL (batch mode) |

**No fallbacks.** Clean, predictable behavior.

## Cost Comparison

| Aspect | Chrome DevTools MCP | crawl4ai API |
|--------|---------------------|--------------|
| **Browser instances** | New per session | Pooled/reused |
| **Parallel processing** | Sequential only | 5-10 concurrent |
| **Token usage** | Full accessibility tree | Pruned markdown |
| **Infrastructure** | MCP server (persistent) | Docker container (on-demand) |

**Estimated improvement:**
- **Speed:** 5-10x faster for batch URLs (parallel vs sequential)
- **Token usage:** ~50-70% reduction (fit_markdown vs accessibility tree)
- **Infrastructure:** Single Docker container vs persistent MCP connection

## File Changes

| File | Change |
|------|--------|
| `skills/distributor-inspector/SKILL.md` | Replace Chrome DevTools MCP calls with crawl4ai API |
| `skills/distributor-inspector/references/` | No changes |
| `scripts/crawl4ai-server.sh` | Docker start/stop script (new) |

## SKILL.md Process Changes

### Current (Chrome DevTools MCP)

```markdown
### Step 1: Navigate to Website
Use Chrome DevTools MCP:
mcp__chrome_devtools__navigate_page(url)

### Step 2: Extract Content
Use Chrome DevTools MCP:
mcp__chrome_devtools__take_snapshot()
```

### Proposed (crawl4ai API)

```markdown
### Step 1: Ensure crawl4ai server running
Check if Docker container is running. If not, prompt user:
"Start crawl4ai server with: docker run -d -p 11235:11235 unclecode/crawl4ai:latest"

### Step 2: Crawl URL(s)
HTTP POST to http://localhost:11235/crawl with fit_markdown configuration.
For batch: Pass array of URLs.

### Step 3: Extract structured data from markdown
LLM parses fit_markdown output for company profile signals:
- Company name
- Products and services
- Brands carried
- Team/employee indicators
- SLA/service mentions
- Geographic coverage
```

## Testing Strategy

### Validation Criteria

1. **Extraction parity**: Compare extracted signals between Chrome DevTools MCP and crawl4ai on same URLs
2. **Scoring consistency**: Scores should match within tolerance (±5 points)
3. **Batch performance**: Measure time for 10 URLs sequential vs parallel

### Test Data

- Use existing `workspace/serp_results.csv` or `workspace/possible_distributors.md` examples
- Include edge cases: JS-heavy sites, simple sites, competitor distributors

## Prerequisites

- Docker installed and running
- `unclecode/crawl4ai:latest` image pulled
- Port 11235 available

## Open Questions

None - design approved by user on 2026-02-25.