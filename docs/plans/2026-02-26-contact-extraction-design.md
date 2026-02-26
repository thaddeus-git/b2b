# Contact Extraction for Distributor Inspector

**Date:** 2026-02-26
**Status:** Approved
**Author:** Claude + User collaboration

## Problem Statement

The distributor-inspector skill currently extracts company profile data (products, services, brands, geography, team, SLA) but does not collect contact information. For sales outreach, users need phone, email, address, LinkedIn, and other contact channels.

## Goal

Add automatic contact extraction to the distributor-inspector skill. Always extract contacts for every inspection, detect country/language, and auto-search for LinkedIn if not found on the website.

## What to Extract

### Standard Fields (always extracted)

| Field | Description |
|-------|-------------|
| Phone | Phone numbers including international formats |
| Email | Email addresses |
| Address | Physical address (street, city, postal code, country) |
| WhatsApp | wa.me links or phone numbers labeled for WhatsApp |
| Website | If different from inspected URL |
| Company LinkedIn | LinkedIn company page |
| Country | Detected from TLD, address, lang attribute |
| Language | Detected from content |

### Additional Channels (if found)

- YouTube
- Twitter/X
- Facebook
- Instagram
- Telegram
- WeChat
- Line
- KakaoTalk
- Any other social/messaging platforms

## Output Format

Add Contact section after Company Profile:

```markdown
## {company_name} - {grade} ({score}/100)

**URL:** {url}
**Country:** {country} (detected from TLD/address/content)
**Language:** {language} (detected from content)
**Tags:** {tag1}, {tag2}
**Action:** {action}

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
- **Additional Channels:** {youtube}, {twitter}, {facebook}, etc. or "None detected"

### Key Signals
{signals_list}

### Scoring Details
...
```

## Process Changes

Add Step 3 between Extract Company Profile and Categorize:

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
- Report detected country and language in output

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

## LinkedIn Auto-Search Logic

When LinkedIn is not found on the inspected website:

1. Detect country from TLD (.de, .fr, .at, .es, etc.) and content
2. Use google-search skill with detected locale
3. Search query: `"{domain}" linkedin`
4. If found, add URL to Contact section
5. If not found, output: `LinkedIn: Not found`

**Example:**
- URL: `https://ziler-service.de/impressum`
- Detected country: Germany (from .de TLD, German content)
- LinkedIn not found on page
- Search: `google-search skill with query "ziler-service.de linkedin" locale "de-DE"`
- Result added to Contact section

## Country/Language Detection

**Primary signals:**
- URL TLD (.de, .fr, .at, .es, .it, .nl, .co.kr, .co.uk, etc.)
- HTML `lang` attribute (`<html lang="de">`)
- Address parsing (country names, postal codes)

**Secondary signals:**
- Content language (German text, French text, etc.)
- Phone number country codes (+49, +33, +43, etc.)

Report in output as:
```markdown
**Country:** Germany (detected from .de TLD, address)
**Language:** German (detected from content)
```

## File Changes

| File | Change |
|------|--------|
| `skills/distributor-inspector/SKILL.md` | Add Contact section to output format, add Step 3, update Process |

## Expected Outcome

Every inspection output will include:
1. Country and language detection
2. Complete contact section with phone, email, address, WhatsApp, website, LinkedIn
3. Additional channels if present (YouTube, Twitter, etc.)
4. Auto-searched LinkedIn if not found on website