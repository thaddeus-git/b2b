# B2B Skills Code Review Report

**Date:** 2026-02-28
**Reviewer:** Claude Code (Automated)
**Scope:** Deep review of lead-enricher and distributor-inspector skills

---

## Summary

| Category | Critical | Important | Minor | Total |
|----------|-----------|------------|--------|-------|
| Bugs & Logic | 1 | 1 | 0 | 2 |
| Security | 0 | 2 | 2 | 4 |
| Error Handling | 0 | 2 | 0 | 2 |
| Code Quality | 0 | 3 | 2 | 5 |
| Consistency | - | 3 | - | 3 |
| Test Coverage | - | 2 | 1 | 3 |

**Files Reviewed:**
- `skills/lead-enricher/scripts/enrich.py` (947 lines)
- `skills/lead-enricher/scripts/setup.py` (87 lines)
- `skills/lead-enricher/scripts/tests/test_enrich.py` (140 lines)
- `skills/distributor-inspector/scripts/search.py` (251 lines)
- `skills/distributor-inspector/scripts/setup.py` (85 lines)

---

## 1. Bugs & Logic Errors

### CRITICAL

#### 1.1 Duplicate Key in Dict
**File:** `skills/distributor-inspector/scripts/search.py:90-91`

```python
"NG": "Nigeria", "KE": "Kenya", "NG": "Nigeria", "ZA": "South Africa",
```

**Problem:** `NG` (Nigeria) appears twice. Python dicts keep only the last value for duplicate keys, so the first `NG` entry is silently overwritten. This could cause confusion when debugging.

**Fix:**
```python
# Remove duplicate NG entry
"NG": "Nigeria", "KE": "Kenya", "ZA": "South Africa",
```

---

### IMPORTANT

#### 1.2 Hardcoded Default Country
**File:** `skills/lead-enricher/scripts/enrich.py:291`

```python
return "DE"  # Default to Germany for German leads
```

**Problem:** Hardcoded default may not be appropriate for non-German leads. Should come from config or use a smarter default based on email domain TLD.

**Recommendation:** Consider adding more country detection or making default configurable.

---

## 2. Security

### IMPORTANT

#### 2.1 API Key Partial Exposure in Test Mode
**File:** `skills/lead-enricher/scripts/enrich.py:924`

```python
print(f"API key found: {api_key[:8]}...")
```

**Problem:** Shows first 8 characters of API key. While not the full key, this still reveals sensitive information in logs/screenshots.

**Fix:**
```python
# Mask more of the key - show only last 4 chars
print(f"API key configured: ...{api_key[-4:]}")
```

---

#### 2.2 Environment Variable Detection Reveals Key Status
**File:** `skills/distributor-inspector/scripts/search.py:237`

```python
"env_var_set": bool(os.environ.get("BRIGHTDATA_SERP_API_KEY"))
```

**Problem:** Reveals whether API key is set in environment, which could help attackers target systems with keys configured.

**Fix:** Remove this from the response or mask it:
```python
"env_var_set": bool(os.environ.get("BRIGHTDATA_SERP_API_KEY", ""))
# Or remove entirely from response
```

---

### MINOR

#### 2.3 Bare Exception Handler Silences Errors
**File:** `skills/lead-enricher/scripts/enrich.py:313-314`

```python
except Exception:
    pass
```

**Problem:** Silent exception swallowing makes debugging difficult. Network errors, SSL issues, and other problems are hidden.

**Fix:**
```python
except (aiohttp.ClientError, asyncio.TimeoutError, ssl.SSLError) as e:
    logger.debug(f"Direct website check failed: {e}")
except Exception:
    pass  # Keep as fallback but log if possible
```

---

#### 2.4 Same Issue in search.py
**File:** `skills/distributor-inspector/scripts/search.py:170`

```python
except Exception as e:
    return {"error": str(e), ...}
```

**Problem:** While it returns the error, catching broad `Exception` can hide specific error types that might need different handling.

---

## 3. Error Handling

### IMPORTANT

#### 3.1 No CSV Column Validation
**File:** `skills/lead-enricher/scripts/enrich.py:824-827`

```python
with open(input_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter="\t")
    leads = list(reader)
```

**Problem:** No validation that required columns (`full_name`, `company_name`, `work_phone_number`, `work_email`) exist in the CSV. If columns are missing, the script will run but produce empty results.

**Fix:**
```python
REQUIRED_COLUMNS = {"full_name", "company_name", "work_phone_number", "work_email"}

reader = csv.DictReader(f, delimiter="\t")
if not REQUIRED_COLUMNS.issubset(set(reader.fieldnames or [])):
    missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
    return {"error": f"Missing required columns: {missing}", "success": False}
leads = list(reader)
```

---

#### 3.2 Potential IndexError
**File:** `skills/lead-enricher/scripts/enrich.py:856`

```python
fieldnames = list(enriched[0].keys())
```

**Problem:** If `enriched` is empty (all leads filtered out), this will raise `IndexError`.

**Fix:**
```python
if not enriched:
    return {"error": "No valid leads to process", "success": False}
fieldnames = list(enriched[0].keys())
```

---

#### 3.3 Batch Search Has No Partial Failure Handling
**File:** `skills/distributor-inspector/scripts/search.py:178-206`

```python
async def search_batch(...):
    tasks = [search_google(q, ...) for q in queries]
    all_results = await asyncio.gather(*tasks)
    return {"success": True, ...}
```

**Problem:** If some searches fail and others succeed, the batch returns `success: True` with no indication of partial failures.

**Fix:**
```python
all_results = await asyncio.gather(*tasks, return_exceptions=True)
failed = [q for q, r in zip(queries, all_results) if isinstance(r, Exception)]
if failed:
    return {
        "success": len(failed) < len(queries),  # True if some succeeded
        "partial_failure": len(failed) > 0,
        "failed_queries": failed,
        ...
    }
```

---

## 4. Code Quality

### IMPORTANT

#### 4.1 DRY: Repeated Code Patterns
**Files:** `skills/lead-enricher/scripts/enrich.py:196-214, 383-402, 445-507, 510-559, 562-617`

**Problem:** The following patterns are repeated 6+ times:
- `get_api_key()` function
- `location_map` dictionary
- BrightDataClient setup with `validate_token=False, auto_create_zones=False`

**Recommendation:** Extract to a shared utility module:

```python
# skills/shared/brightdata_utils.py
from brightdata import BrightDataClient

LOCATION_MAP = {
    "DE": "Germany", "AT": "Austria", "CH": "Switzerland",
    "FR": "France", "ES": "Spain", "NL": "Netherlands",
    ...
}

async def create_client(api_key: str):
    return BrightDataClient(
        token=api_key,
        validate_token=False,
        auto_create_zones=False,
    )
```

---

#### 4.2 Hardcoded Skip Domains
**File:** `skills/lead-enricher/scripts/enrich.py:671-674`

```python
skip_domains = ["linkedin.com", "facebook.com", "instagram.com",
                "twitter.com", "youtube.com", "wikipedia.org"]
```

**Problem:** Should be a module-level constant for maintainability.

**Fix:**
```python
SKIP_DOMAINS = frozenset([
    "linkedin.com", "facebook.com", "instagram.com",
    "twitter.com", "youtube.com", "wikipedia.org"
])
```

---

#### 4.3 Magic Number for Confidence Threshold
**File:** `skills/lead-enricher/scripts/enrich.py:773`

```python
if confidence < min_confidence and confidence >= 0.5:
```

**Problem:** `0.5` is a magic number. Should be a named constant.

**Fix:**
```python
MEDIUM_CONFIDENCE_THRESHOLD = 0.5
# ...
if confidence < min_confidence and confidence >= MEDIUM_CONFIDENCE_THRESHOLD:
```

---

### MINOR

#### 4.4 Empty if/else Block
**File:** `skills/lead-enricher/scripts/enrich.py:783-785`

```python
if person_is_company and not is_generic_email:
    # Can verify via email domain
    pass  # Already handled above
```

**Problem:** The `pass` with comment is awkward. This branch could be restructured or removed.

**Recommendation:** Either remove the branch or restructure:
```python
# Only flag if we can't verify AND have generic email
if person_is_company and is_generic_email and not result["notes"]:
    result["notes"] = "Person name equals company name with generic email. Verify manually."
```

---

#### 4.5 Limited Location Map in search_linkedin_person
**File:** `skills/lead-enricher/scripts/enrich.py:528`

```python
location_map = {"DE": "Germany", "AT": "Austria", "CH": "Switzerland"}
```

**Problem:** Only supports DE, AT, CH while other search functions support more countries (FR, ES, NL, BE, IT, PL).

**Fix:** Use the shared `LOCATION_MAP` constant.

---

## 5. Cross-Skill Consistency

| Area | lead-enricher | distributor-inspector | Issue |
|------|---------------|----------------------|-------|
| Config path | `~/.claude/lead-enricher/` | `~/.claude/distributor-inspector/` | Different directories - acceptable but should be documented |
| `get_api_key()` | Duplicated in enrich.py | Duplicated in search.py | **Should be in shared module** |
| `setup.py` | Installs `pandas`, `thefuzz` | No extra packages | Different dependency sets |
| Tests | ✅ 26 unit tests | ❌ No tests | **distributor-inspector needs tests** |
| Error format | `{"error": "...", "success": False}` | `{"error": "...", "success": False}` | ✅ Consistent |
| CLI error handling | Exits with code 1 | Exits with code 1 | ✅ Consistent |

---

## 6. Test Coverage

### Current Coverage

| Skill | Unit Tests | Integration Tests | Coverage |
|-------|-----------|-------------------|----------|
| lead-enricher | ✅ 26 tests | ❌ None | Good utility coverage, no API tests |
| distributor-inspector | ❌ None | ❌ None | **No automated testing** |

### Recommended Additions

#### For lead-enricher:
1. **Integration tests** with mocked BrightData API
2. **Edge case tests** for:
   - Empty CSV file
   - CSV with missing columns
   - Malformed email addresses
   - Unicode in company names

#### For distributor-inspector:
1. **Create `tests/test_search.py`** with tests for:
   - `country_code_to_location()`
   - `search_google()` error handling
   - `search_batch()` partial failures
   - API key retrieval

---

## Action Items

### Priority 1 (Fix Immediately)

| # | Issue | File | Effort |
|---|-------|------|--------|
| 1 | Duplicate key bug | search.py:90 | 1 line |

### Priority 2 (Fix This Week)

| # | Issue | File | Effort |
|---|-------|------|--------|
| 2 | API key exposure | enrich.py:924 | 1 line |
| 3 | API key exposure | search.py:237 | 1 line |
| 4 | CSV column validation | enrich.py:824 | 5 lines |
| 5 | IndexError protection | enrich.py:856 | 3 lines |
| 6 | Create shared utils module | new file | 30 min |
| 7 | Add tests for distributor-inspector | new file | 20 min |

### Priority 3 (Nice to Have)

| # | Issue | File | Effort |
|---|-------|------|--------|
| 8 | Extract constants | enrich.py | 10 min |
| 9 | Improve exception handling | enrich.py, search.py | 15 min |
| 10 | Add integration tests | tests/ | 30 min |

---

## Conclusion

The B2B skills codebase is reasonably well-structured with good documentation. The main concerns are:

1. **Critical bug** in search.py with duplicate dict key
2. **Security** around API key exposure
3. **DRY violations** with repeated code patterns across files
4. **Missing tests** for distributor-inspector

Overall code quality is acceptable for a skills project, With the fixes above, it would be production-ready.
