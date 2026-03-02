# SDK Testing & Dependency Management Design

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Prevent the "wrong package installed" bug from recurring and standardize dependency management across skills.

**Architecture:** Add smoke tests that verify the correct Bright Data SDK is installed (with BrightDataClient). Replace ad-hoc requirements.txt with pyproject.toml + uv for reproducible builds.

**Tech Stack:** Python 3.11+, pytest, brightdata-sdk, uv package manager

---

## Problem Statement

**Bug encountered:** User installed `brightdata==0.4.0.4` (third-party wrapper) instead of `brightdata-sdk==2.2.1` (official SDK). The wrong package doesn't have `BrightDataClient`, causing ImportError at runtime.

**Root cause:** No tests verified SDK imports, and no locked dependencies.

---

## Section 1: SDK Smoke Test

**Location:** `skills/lead-enricher/scripts/tests/test_enrich.py` (add to existing)

**Test code:**
```python
class TestBrightDataSDK:
    """Smoke tests for Bright Data SDK installation."""

    def test_sdk_imports_brightdata_client(self):
        """Verify the correct SDK is installed with BrightDataClient."""
        from brightdata import BrightDataClient
        assert BrightDataClient is not None

    def test_sdk_has_search_methods(self):
        """Verify SDK has expected search methods."""
        from brightdata import BrightDataClient
        client = BrightDataClient(token="test", validate_token=False)
        assert hasattr(client, 'search')
        assert hasattr(client.search, 'google')
```

**Why this works:**
- `brightdata==0.4.0.4` (wrong package) → ImportError on `BrightDataClient`
- `brightdata-sdk==2.2.1` (correct package) → Import succeeds

---

## Section 2: Dependency Management with pyproject.toml + uv

**Files to create:**

```
skills/lead-enricher/scripts/
├── pyproject.toml    # NEW: defines dependencies + dev dependencies
└── uv.lock           # NEW: auto-generated lock file
```

**pyproject.toml:**
```toml
[project]
name = "lead-enricher"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "brightdata-sdk>=2.2.0",
    "aiohttp>=3.9.0",
    "thefuzz>=0.22.0",
    "rapidfuzz>=3.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

**Usage:**
```bash
# Setup (one-time)
cd skills/lead-enricher/scripts
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"

# Run tests
uv run pytest tests/ -v
```

---

## Section 3: Apply to Both Skills + Shared Module

**Files to create/modify:**

```
skills/
├── shared/
│   └── pyproject.toml              # NEW: shared dependencies
├── lead-enricher/scripts/
│   ├── pyproject.toml              # NEW
│   └── requirements.txt            # DELETE (replaced)
└── distributor-inspector/scripts/
    ├── pyproject.toml              # NEW
    └── requirements.txt            # DELETE (replaced)
```

**Shared pyproject.toml** (for `brightdata_utils.py`):
```toml
[project]
name = "b2b-shared"
version = "0.1.0"
dependencies = [
    "brightdata-sdk>=2.2.0",
]
```

**Distributor-inspector pyproject.toml:**
```toml
[project]
name = "distributor-inspector"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "brightdata-sdk>=2.2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
]
```

**Delete old requirements.txt files** - replaced by pyproject.toml

---

## Implementation Tasks

1. Add SDK smoke tests to lead-enricher
2. Add SDK smoke tests to distributor-inspector
3. Create pyproject.toml for lead-enricher
4. Create pyproject.toml for distributor-inspector
5. Create pyproject.toml for shared module
6. Delete old requirements.txt files
7. Regenerate venvs with uv
8. Run all tests to verify
