# Company Profiler Sub-skill

## Purpose

Extract and structure company profile information from website content.

---

## Company Profile Fields

Extract the following from website content:

| Field | Description |
|-------|-------------|
| **Products** | Product categories and specific offerings |
| **Services** | Service offerings (maintenance, support, training) |
| **Brands** | Brands carried/distributed |
| **Geography** | Market coverage area (cities, regions, countries) |
| **Team** | Team size, capability indicators, employee mentions |
| **SLA** | Service level agreement mentions, response times |

---

## Extraction Process

### Step 1: Navigate and Capture

Use Playwright MCP tools:
1. `browser_navigate` - load the website URL
2. `browser_snapshot` - capture accessibility tree content

### Step 2: Parse Company Profile

From the accessibility snapshot, extract:

**Company name:**
- From page title, header, or About section
- Use legal name from Impressum if available (EU sites)

**Products:**
- Look for product categories, catalog pages
- Identify commercial vs consumer focus
- Note specific product types (scrubbers, sweepers, robots)

**Services:**
- After-sales support
- Maintenance offerings
- Training programs
- Installation services

**Brands:**
- "Our brands", "partners", "distributors of" sections
- Brand logos in footer or product pages
- Authorized dealer certifications

**Geography:**
- Coverage area mentions
- Service regions
- Customer locations in case studies

**Team:**
- Employee count mentions
- Team structure (sales, technical, support)
- "About us" or "Company" page details

**SLA:**
- Response time guarantees
- Service commitments
- Support availability (24/7, business hours)

---

## Error Handling

### Navigation Failure

If the website cannot be accessed:
1. Check the URL is correct and accessible
2. Verify the website is not blocking automated access
3. Return error with the URL for manual review

### Empty Content

If the accessibility snapshot is empty or missing key information:
1. Try scrolling the page with `browser_press_key` to load lazy content
2. Check if the page requires JavaScript interaction
3. Return error with URL for manual review

---

## Company Profile Output Format

```markdown
### Company Profile
- **Products:** {products}
- **Services:** {services}
- **Brands:** {brands}
- **Geography:** {geography}
- **Team:** {team_presence}
- **SLA:** {sla_mentions}
```

---

## Detection Tips

1. **Check multiple pages:** Home, About, Products, Services, Contact
2. **Footer intelligence:** Brand logos, certifications, quick links
3. **Impressum (EU):** Legal info, registered address, contacts
4. **Case studies:** Reveal target customers and capabilities
5. **News/Press:** Recent developments, partnerships, expansions
