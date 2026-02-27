# crawl4ai Integration Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Replace Chrome DevTools MCP with crawl4ai API server for website content extraction in the distributor-inspector skill, enabling batch processing and improving performance.

**Architecture:** crawl4ai Docker container runs locally on port 11235. SKILL.md makes HTTP POST requests to crawl URLs and extract fit_markdown content. LLM parses the markdown output for company profile signals, scoring remains unchanged.

**Tech Stack:** crawl4ai (Docker), HTTP API, Python (optional helper script), existing skill framework

---

## Task 1: Create crawl4ai Server Script

**Files:**
- Create: `scripts/crawl4ai-server.sh`

**Step 1: Create the server management script**

```bash
#!/bin/bash
# crawl4ai-server.sh - Manage crawl4ai Docker container for distributor-inspector

set -e

CONTAINER_NAME="crawl4ai"
IMAGE_NAME="unclecode/crawl4ai:latest"
PORT=11235

start() {
    if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        echo "✓ crawl4ai server already running on port ${PORT}"
        exit 0
    fi

    echo "Starting crawl4ai server..."
    docker run -d \
        --name ${CONTAINER_NAME} \
        -p ${PORT}:${PORT} \
        ${IMAGE_NAME}

    echo "✓ crawl4ai server started on port ${PORT}"
    echo "  API endpoint: http://localhost:${PORT}/crawl"
}

stop() {
    if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        echo "✓ crawl4ai server not running"
        exit 0
    fi

    echo "Stopping crawl4ai server..."
    docker stop ${CONTAINER_NAME} && docker rm ${CONTAINER_NAME}
    echo "✓ crawl4ai server stopped"
}

status() {
    if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        echo "✓ crawl4ai server running on port ${PORT}"
        echo "  Container: ${CONTAINER_NAME}"
        echo "  API endpoint: http://localhost:${PORT}/crawl"
    else
        echo "✗ crawl4ai server not running"
        echo "  Run: $0 start"
        exit 1
    fi
}

case "${1:-status}" in
    start)  start ;;
    stop)   stop ;;
    status) status ;;
    restart) stop; start ;;
    *)
        echo "Usage: $0 {start|stop|status|restart}"
        exit 1
        ;;
esac
```

**Step 2: Make script executable**

Run: `chmod +x scripts/crawl4ai-server.sh`
Expected: No output, script becomes executable

**Step 3: Test the script**

Run: `./scripts/crawl4ai-server.sh status`
Expected: Shows "crawl4ai server not running" (since not started yet)

**Step 4: Commit**

```bash
git add scripts/crawl4ai-server.sh
git commit -m "feat: add crawl4ai server management script

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 2: Update SKILL.md Prerequisites Section

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md:14-26` (Prerequisites section)

**Step 1: Replace prerequisites section**

Replace lines 14-26 (the entire Prerequisites section) with:

```markdown
## Prerequisites

This skill requires **crawl4ai** for website content extraction.

### Quick Start

1. Ensure Docker is installed and running
2. Start the crawl4ai server:
   ```bash
   ./scripts/crawl4ai-server.sh start
   ```
3. Verify the server is running:
   ```bash
   ./scripts/crawl4ai-server.sh status
   ```

### Manual Setup (Alternative)

```bash
docker run -d --name crawl4ai -p 11235:11235 unclecode/crawl4ai:latest
```

The server runs on `http://localhost:11235` with the `/crawl` endpoint.

For enrichment searches, this skill uses the **google-search** skill (Bright Data SERP API). Ensure it's configured with valid API credentials.
```

**Step 2: Verify the change**

Run: `grep -A 20 "## Prerequisites" skills/distributor-inspector/SKILL.md`
Expected: Shows the new prerequisites section with crawl4ai instructions

**Step 3: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "feat: update prerequisites for crawl4ai

Replace Chrome DevTools MCP prerequisite with crawl4ai Docker server.
Includes quick start script and manual setup alternative.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 3: Update SKILL.md Process Section

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md:188-214` (Process section Steps 1-2)

**Step 1: Replace Process Steps 1-2**

Replace lines 188-214 (from "## Process" through the end of Step 2: Extract Content) with:

```markdown
## Process

### Step 1: Ensure crawl4ai Server Running

Check if the crawl4ai server is running:

```bash
./scripts/crawl4ai-server.sh status
```

If not running, start it:

```bash
./scripts/crawl4ai-server.sh start
```

If the server is unavailable, fail with:

```
Error: crawl4ai server not running.

Start with: ./scripts/crawl4ai-server.sh start

Or manually: docker run -d --name crawl4ai -p 11235:11235 unclecode/crawl4ai:latest
```

### Step 2: Crawl URL(s)

**Single URL:**

POST to `http://localhost:11235/crawl` with this payload:

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

**Batch URLs (5-10 concurrent):**

```json
{
  "urls": ["https://url1.com", "https://url2.com", "https://url3.com"],
  "browser_config": { ... },
  "crawler_config": { ... }
}
```

**Response format:**

```json
[
  {
    "url": "https://example.com",
    "success": true,
    "markdown": {
      "fit_markdown": "Company Name\n\nProducts and services..."
    }
  }
]
```

### Step 3: Extract Structured Data from Markdown

Parse the `fit_markdown` content for:
- Company name
- Products and services
- Brands carried
- Team/employee indicators
- SLA/service mentions
- Geographic coverage

If `success: false` or empty markdown, return error with URL for manual review.

**Step 4: Categorize**
```

Note: Keep the rest of the Process section (Step 3: Categorize through Step 5: Route) unchanged.

**Step 2: Verify the change**

Run: `grep -A 80 "## Process" skills/distributor-inspector/SKILL.md | head -90`
Expected: Shows new Steps 1-3 with crawl4ai API calls, and Step 4: Categorize

**Step 3: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "feat: replace Chrome DevTools with crawl4ai API

- Add server check step with fail-fast error
- Add crawl API payload with fit_markdown extraction
- Add batch URL support for parallel processing
- Extract structured data from markdown response

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 4: Update SKILL.md Error Handling Section

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md:249-276` (Error Handling section)

**Step 1: Replace Error Handling section**

Replace lines 249-276 (entire Error Handling section) with:

```markdown
## Error Handling

### crawl4ai Server Not Running

If the crawl4ai server is not running, fail immediately:

```
Error: crawl4ai server not running.

Start with: ./scripts/crawl4ai-server.sh start

Or manually: docker run -d --name crawl4ai -p 11235:11235 unclecode/crawl4ai:latest
```

### Crawl Failure

If `success: false` in response:
1. Return error with the URL
2. Suggest manual review
3. Continue to next URL (batch mode)

### Empty Content

If `fit_markdown` is empty:
1. Return error with URL for manual review
2. Do NOT retry with different settings
3. Continue to next URL (batch mode)

### Rate Limiting

crawl4ai has built-in retry with exponential backoff. No manual handling needed.
```

**Step 2: Verify the change**

Run: `grep -A 30 "## Error Handling" skills/distributor-inspector/SKILL.md`
Expected: Shows new error handling section with fail-fast approach

**Step 3: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "feat: update error handling for crawl4ai

Replace Chrome DevTools errors with crawl4ai-specific errors.
Fail fast on server not running, empty content, and crawl failures.
No fallbacks - clean, predictable behavior.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 5: Update SKILL.md Description

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md:3-4` (description in frontmatter)

**Step 1: Update description**

Replace line 3:

```markdown
description: Use when evaluating websites as potential distributors for OrionStar Robotics (cleaning robots). Requires Chrome DevTools MCP. Use when needing to score companies against ICP criteria, categorize by niche market, or identify competitor distributors for sales outreach.
```

With:

```markdown
description: Use when evaluating websites as potential distributors for OrionStar Robotics (cleaning robots). Requires crawl4ai Docker server. Use when needing to score companies against ICP criteria, categorize by niche market, or identify competitor distributors for sales outreach. Supports batch processing.
```

**Step 2: Verify the change**

Run: `head -5 skills/distributor-inspector/SKILL.md`
Expected: Shows updated description with "crawl4ai Docker server" and "Supports batch processing"

**Step 3: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "docs: update skill description for crawl4ai

- Replace Chrome DevTools MCP with crawl4ai Docker server
- Add batch processing mention

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 6: Update Design Document with Implementation Status

**Files:**
- Modify: `docs/plans/2026-02-25-crawl4ai-integration-design.md` (add implementation section)

**Step 1: Add implementation section at the end**

Append to the file:

```markdown

## Implementation Status

- [x] Design approved: 2026-02-25
- [ ] Task 1: Create crawl4ai server script
- [ ] Task 2: Update SKILL.md prerequisites
- [ ] Task 3: Update SKILL.md process section
- [ ] Task 4: Update SKILL.md error handling
- [ ] Task 5: Update SKILL.md description
- [ ] Task 7: Test with sample URLs
- [ ] Task 8: Validate extraction parity
```

**Step 2: Commit**

```bash
git add docs/plans/2026-02-25-crawl4ai-integration-design.md
git commit -m "docs: add implementation status tracking

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 7: Test with Sample URLs

**Files:**
- No file changes (manual testing)

**Step 1: Start crawl4ai server**

Run: `./scripts/crawl4ai-server.sh start`
Expected: Docker container starts, shows "crawl4ai server started on port 11235"

**Step 2: Test single URL crawl**

Run:
```bash
curl -X POST http://localhost:11235/crawl \
  -H "Content-Type: application/json" \
  -d '{
    "urls": ["https://karcher.com"],
    "browser_config": {"type": "BrowserConfig", "params": {"headless": true}},
    "crawler_config": {"type": "CrawlerRunConfig", "params": {"page_timeout": 60000}}
  }'
```
Expected: JSON response with `success: true` and markdown content

**Step 3: Test batch URL crawl**

Run:
```bash
curl -X POST http://localhost:11235/crawl \
  -H "Content-Type: application/json" \
  -d '{
    "urls": ["https://karcher.com", "https://nilfisk.com"],
    "browser_config": {"type": "BrowserConfig", "params": {"headless": true}},
    "crawler_config": {"type": "CrawlerRunConfig", "params": {"page_timeout": 60000}}
  }'
```
Expected: JSON array with 2 results

**Step 4: Verify fit_markdown extraction**

Run the single URL test again and check that `fit_markdown` contains relevant company information (products, services, brands).

---

## Task 8: Validate Extraction Parity

**Files:**
- No file changes (validation testing)

**Step 1: Select test URLs**

Use 3-5 URLs from `workspace/serp_results.csv` or `workspace/possible_distributors.md`

**Step 2: Extract with current Chrome DevTools MCP**

For each URL:
1. Use `mcp__chrome_devtools__navigate_page(url)`
2. Use `mcp__chrome_devtools__take_snapshot()`
3. Record extracted signals (company name, products, brands, team, geography, SLA)

**Step 3: Extract with crawl4ai**

For each URL:
1. POST to crawl4ai API
2. Parse `fit_markdown`
3. Record extracted signals

**Step 4: Compare results**

| Metric | Target |
|--------|--------|
| Company name match | 90%+ |
| Product/service signals | 80%+ |
| Brand mentions | 90%+ |
| Team indicators | 70%+ |
| Geography | 80%+ |
| SLA mentions | 60%+ |

**Step 5: Adjust PruningContentFilter threshold if needed**

If extraction quality is low, adjust `threshold` in the payload:
- Lower threshold (0.4-0.5) = more content, more noise
- Higher threshold (0.7-0.8) = less content, cleaner signal

---

## Summary

| Task | Description | Files |
|------|-------------|-------|
| 1 | Create server script | `scripts/crawl4ai-server.sh` |
| 2 | Update prerequisites | `skills/distributor-inspector/SKILL.md:14-26` |
| 3 | Update process section | `skills/distributor-inspector/SKILL.md:188-214` |
| 4 | Update error handling | `skills/distributor-inspector/SKILL.md:249-276` |
| 5 | Update description | `skills/distributor-inspector/SKILL.md:3-4` |
| 6 | Update design doc | `docs/plans/2026-02-25-crawl4ai-integration-design.md` |
| 7 | Test with sample URLs | Manual testing |
| 8 | Validate extraction parity | Manual testing |

**Key changes:**
- Chrome DevTools MCP → crawl4ai API server
- Sequential → parallel batch processing (5-10 URLs)
- Accessibility tree → fit_markdown (50-70% token reduction)
- MCP dependency → Docker dependency