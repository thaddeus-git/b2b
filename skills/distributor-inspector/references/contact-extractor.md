# Contact Extractor Sub-skill

## Purpose

Extract contact information from website content with precision and completeness.

---

## Standard Fields to Extract

**Contact details:**
- Phone numbers (including international formats)
- Email addresses
- Physical address (street, city, postal code, country)
- WhatsApp contact (wa.me links or phone numbers labeled for WhatsApp)
- Website (if different from the URL being inspected)
- Company LinkedIn page

---

## Headquarters vs Multiple Locations

**If one address found:**
- Report as both Address and Headquarters

**If multiple addresses found:**
1. Look for signals: "headquarters", "head office", "corporate", "main office", "registered office", "Hauptsitz" (DE), "siège social" (FR)
2. EU sites: Impressum page usually has the legal/registered address
3. Report Headquarters separately from other locations
4. Note total number of locations if discoverable

**Location field format:**
- **Headquarters:** {city}, {region/state}, {country} (or full address if single location)
- **Additional Locations:** Count and list if multiple offices/branches found

---

## Country and Language Detection

- Infer from URL TLD, page language attribute, and address
- Extract city/region from address for sales territory context
- Report detected country and language in output header

---

## Additional Channels to Detect

- YouTube, Twitter/X, Facebook, Instagram, Telegram, WeChat, Line, KakaoTalk
- Any other social or messaging platforms used for contact
- Report as "Additional Channels" if found

---

## Common Contact Page Locations

- Check footer, "Contact", "Impressum", "About" sections
- Many EU sites have legal pages with complete contact info

---

## LinkedIn Search (Mandatory if Not Found)

**If LinkedIn not found on website, you MUST search for it:**

1. Run the search script from the distributor-inspector skill directory:
   ```bash
   python3 scripts/search.py "{company_name} linkedin" "{country}" "{language}" "5"
   ```
2. Parse the JSON output and extract the LinkedIn URL from the first matching result
3. If found, add the LinkedIn URL to the Contact section
4. If not found after search, report: "Not found (searched)"

**This step is mandatory** - do not skip it. LinkedIn is critical for sales outreach preparation.

---

## Contact Output Format

```markdown
### Contact
- **Phone:** {phone} or "Not found"
- **Email:** {email} or "Not found"
- **Headquarters:** {city}, {region}, {country} (or full address if single location)
- **Address:** {full_address} or "Not found"
- **Additional Locations:** {count} offices/branches (list if found) or "Single location"
- **WhatsApp:** {whatsapp_number} or "Not found"
- **Website:** {main_website} or "Same as URL"
- **LinkedIn:** {company_linkedin_url} or "Not found (searched)"
- **Additional Channels:** {youtube}, {twitter}, {facebook}, {instagram}, etc. or "None detected"
```

---

## Extraction Tips

1. **Phone numbers:** Look for multiple formats (+49, 0049, local)
2. **Email:** Check for obfuscated formats (info [at] domain [dot] com)
3. **WhatsApp:** Look for wa.me links or phone numbers with WhatsApp labels
4. **Social links:** Check footer icons and header navigation
5. **Addresses:** Parse structured address blocks, not just inline text
