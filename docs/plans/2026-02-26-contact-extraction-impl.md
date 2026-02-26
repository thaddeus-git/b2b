# Add Contact Extraction to Distributor Inspector

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add automatic contact extraction to distributor-inspector skill. Extract phone, email, address, WhatsApp, LinkedIn, country/language, and additional social channels for every inspection.

**Files to modify:**
- `skills/distributor-inspector/SKILL.md`

---

## Task 1: Add Country/Language to Output Header

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md` (Output Format section)

**Step 1: Update the output header format**

Find the output format section (around line 104-130) and update the header to include Country and Language:

```markdown
## {company_name} - {grade} ({score}/100)

**URL:** {url}
**Country:** {country} (detected from TLD/address/content)
**Language:** {language} (detected from content)
**Tags:** {tag1}, {tag2}
**Action:** {action}
**Play:** {play} (optional - only if competitor footprint detected)
```

**Step 2: Verify the change**

Run: `grep -A 8 "## {company_name}" skills/distributor-inspector/SKILL.md | head -10`
Expected: Shows Country and Language fields in header

**Step 3: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "feat: add country/language detection to output header

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 2: Add Contact Section to Output Format

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md` (Output Format section)

**Step 1: Add Contact section after Company Profile**

Find the Company Profile section and add Contact section immediately after it:

```markdown
### Company Profile
- **Products:** {products}
- **Services:** {services}
- **Brands:** {brands}
- **Geography:** {geography}
- **Team:** {team_presence}
- **SLA:** {sla_mentions}

### Contact
- **Phone:** {phone} or "Not found"
- **Email:** {email} or "Not found"
- **Address:** {full_address} or "Not found"
- **WhatsApp:** {whatsapp_number} or "Not found"
- **Website:** {main_website} or "Same as URL"
- **LinkedIn:** {company_linkedin_url} or "Not found"
- **Additional Channels:** {youtube}, {twitter}, {facebook}, {instagram}, etc. or "None detected"

### Key Signals
{signals_list}
```

**Step 2: Verify the change**

Run: `grep -A 15 "### Company Profile" skills/distributor-inspector/SKILL.md | head -20`
Expected: Shows Company Profile, Contact, and Key Signals sections

**Step 3: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "feat: add Contact section to output format

Includes phone, email, address, WhatsApp, website, LinkedIn,
and additional channels.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 3: Add Step 3 to Process Section

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md` (Process section)

**Step 1: Add Contact Extraction step**

Find the Process section and add Step 3 between Extract Company Profile and Categorize. The current flow is:

- Step 1: Navigate and Capture
- Step 2: Extract Company Profile
- Step 3: Categorize (current)
- Step 4: Score (current)
- Step 5: Route (current)

Change to:

- Step 1: Navigate and Capture
- Step 2: Extract Company Profile
- Step 3: Extract Contact Information (NEW)
- Step 4: Categorize (renumbered)
- Step 5: Score (renumbered)
- Step 6: Route (renumbered)

Add after Step 2:

```markdown
### Step 3: Extract Contact Information

From the page content, extract contact details:

**Standard fields to look for:**
- Phone numbers (including international formats)
- Email addresses
- Physical address (street, city, postal code, country)
- WhatsApp contact (wa.me links or phone numbers labeled for WhatsApp)
- Website (if different from the URL being inspected)
- Company LinkedIn page

**Country and language:**
- Infer from URL TLD, page language attribute, and address
- Report detected country and language in output header

**Additional channels to detect:**
- YouTube, Twitter/X, Facebook, Instagram, Telegram, WeChat, Line, KakaoTalk
- Any other social or messaging platforms used for contact
- Report as "Additional Channels" if found

**If LinkedIn not found on website:**
- Use google-search skill to search `"{domain}" linkedin` in the detected country/locale
- Add result to Contact section if found

**Common contact page locations:**
- Check footer, "Contact", "Impressum", "About" sections
- Many EU sites have legal pages with complete contact info
```

**Step 2: Update remaining step numbers**

Renumber:
- Old Step 3: Categorize → Step 4: Categorize
- Old Step 4: Score → Step 5: Score
- Old Step 5: Route → Step 6: Route

**Step 3: Verify the change**

Run: `grep -n "### Step" skills/distributor-inspector/SKILL.md`
Expected: Shows Steps 1-6 with Contact Extraction as Step 3

**Step 4: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "feat: add Contact Extraction step to Process

Extract phone, email, address, WhatsApp, LinkedIn, country/language,
and social channels. Auto-search LinkedIn if not found on website.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 4: Update Other Output Format Templates

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md` (Output Format section)

**Step 1: Add Contact section to service-provider-prospect template**

Find the service-provider-prospect output format and add Contact section:

```markdown
**For service-provider-prospect (cleaning services):**

```markdown
## {company_name} - service-provider-prospect

**URL:** {url}
**Country:** {country}
**Language:** {language}
**Tags:** cleaning-services-provider
**Action:** service-provider-prospect

### Company Profile
- **Services:** {services}
- **Equipment used:** {equipment_brands_if_known}
- **Team:** {team_size}
- **Geography:** {geography}

### Contact
- **Phone:** {phone} or "Not found"
- **Email:** {email} or "Not found"
- **Address:** {full_address} or "Not found"
- **WhatsApp:** {whatsapp_number} or "Not found"
- **Website:** {main_website} or "Same as URL"
- **LinkedIn:** {company_linkedin_url} or "Not found"
- **Additional Channels:** {youtube}, {twitter}, {facebook}, {instagram}, etc. or "None detected"

### Note
This is a cleaning SERVICE provider, not an equipment distributor. They may be interested in:
- Purchasing robots for their own operations
- Becoming a referral partner
- Insights into local cleaning market
```
```

**Step 2: Add Contact section to route-to-ka template**

Find the route-to-ka output format and add Contact section similarly.

**Step 3: Add Contact section to pure-2c-retail template**

Find the pure-2c-retail exclude output format and add Contact section similarly.

**Step 4: Verify the changes**

Run: `grep -c "### Contact" skills/distributor-inspector/SKILL.md`
Expected: 4 or more (main template + 3 special templates)

**Step 5: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "feat: add Contact section to all output templates

service-provider-prospect, route-to-ka, and pure-2c-retail templates
now include contact extraction.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Summary

| Task | Description | Files |
|------|-------------|-------|
| 1 | Add Country/Language to output header | `SKILL.md` Output Format |
| 2 | Add Contact section to main output format | `SKILL.md` Output Format |
| 3 | Add Step 3: Extract Contact Information | `SKILL.md` Process |
| 4 | Add Contact section to special templates | `SKILL.md` Output Format |

**Expected outcome:**

Every inspection output will include:
1. Country and language detection in header
2. Complete Contact section with all fields
3. Auto-searched LinkedIn if not found
4. Additional channels if present