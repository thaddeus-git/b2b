# SDK Testing & Dependency Management Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add SDK smoke tests and standardize dependency management with pyproject.toml + uv.

**Architecture:** Add test classes that verify BrightDataClient imports correctly. Replace requirements.txt with pyproject.toml for reproducible builds.

**Tech Stack:** Python 3.11+, pytest, brightdata-sdk, uv package manager

---

## Task 1: Add SDK Smoke Tests to lead-enricher

**Files:**
- Modify: `skills/lead-enricher/scripts/tests/test_enrich.py`

**Step 1: Add the test class to test_enrich.py**

Append to end of file:

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

**Step 2: Run tests to verify they pass**

```bash
cd /Users/thaddeus/skills/b2b/skills/lead-enricher/scripts
source .venv/bin/activate
python -m pytest tests/test_enrich.py::TestBrightDataSDK -v
```

Expected: 2 passed

**Step 3: Commit**

```bash
git add skills/lead-enricher/scripts/tests/test_enrich.py
git commit -m "test(lead-enricher): add SDK smoke tests for BrightDataClient"
```

---

## Task 2: Add SDK Smoke Tests to distributor-inspector

**Files:**
- Modify: `skills/distributor-inspector/scripts/tests/test_search.py`

**Step 1: Add the test class to test_search.py**

Append to end of file (before `if __name__ == "__main__"`):

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

**Step 2: Run tests to verify they pass**

```bash
cd /Users/thaddeus/skills/b2b/skills/distributor-inspector/scripts
source .venv/bin/activate
python -m pytest tests/test_search.py::TestBrightDataSDK -v
```

Expected: 2 passed

**Step 3: Commit**

```bash
git add skills/distributor-inspector/scripts/tests/test_search.py
git commit -m "test(distributor-inspector): add SDK smoke tests for BrightDataClient"
```

---

## Task 3: Create pyproject.toml for lead-enricher

**Files:**
- Create: `skills/lead-enricher/scripts/pyproject.toml`

**Step 1: Create pyproject.toml**

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

**Step 2: Commit**

```bash
git add skills/lead-enricher/scripts/pyproject.toml
git commit -m "feat(lead-enricher): add pyproject.toml for dependency management"
```

---

## Task 4: Create pyproject.toml for distributor-inspector

**Files:**
- Create: `skills/distributor-inspector/scripts/pyproject.toml`

**Step 1: Create pyproject.toml**

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

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

**Step 2: Commit**

```bash
git add skills/distributor-inspector/scripts/pyproject.toml
git commit -m "feat(distributor-inspector): add pyproject.toml for dependency management"
```

---

## Task 5: Create pyproject.toml for shared module

**Files:**
- Create: `skills/shared/pyproject.toml`

**Step 1: Create pyproject.toml**

```toml
[project]
name = "b2b-shared"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "brightdata-sdk>=2.2.0",
]
```

**Step 2: Commit**

```bash
git add skills/shared/pyproject.toml
git commit -m "feat(shared): add pyproject.toml for shared module"
```

---

## Task 6: Delete old requirements.txt files

**Files:**
- Delete: `skills/distributor-inspector/requirements.txt`

**Step 1: Remove requirements.txt**

```bash
git rm skills/distributor-inspector/requirements.txt
```

**Step 2: Commit**

```bash
git commit -m "chore: remove requirements.txt (replaced by pyproject.toml)"
```

---

## Task 7: Update SKILL.md documentation

**Files:**
- Modify: `skills/lead-enricher/SKILL.md`
- Modify: `skills/distributor-inspector/SKILL.md`

**Step 1: Update lead-enricher SKILL.md prerequisites section**

Find the prerequisites section and replace:

```markdown
## Prerequisites

```bash
# Configure Bright Data SERP API
cd skills/lead-enricher
python3 scripts/setup.py
# Then edit ~/.claude/lead-enricher/config.json and add your API key
```
```

With:

```markdown
## Prerequisites

```bash
# Install dependencies with uv
cd skills/lead-enricher/scripts
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"

# Configure Bright Data SERP API
python3 setup.py
# Then edit ~/.claude/lead-enricher/config.json and add your API key
```
```

**Step 2: Update distributor-inspector SKILL.md prerequisites section**

Same pattern - add uv setup instructions.

**Step 3: Commit**

```bash
git add skills/lead-enricher/SKILL.md skills/distributor-inspector/SKILL.md
git commit -m "docs: update SKILL.md with uv setup instructions"
```

---

## Task 8: Run all tests to verify

**Step 1: Run lead-enricher tests**

```bash
cd /Users/thaddeus/skills/b2b/skills/lead-enricher/scripts
source .venv/bin/activate
python -m pytest tests/ -v
```

Expected: 28 passed (26 existing + 2 new SDK tests)

**Step 2: Run distributor-inspector tests**

```bash
cd /Users/thaddeus/skills/b2b/skills/distributor-inspector/scripts
source .venv/bin/activate
python -m pytest tests/ -v
```

Expected: All tests pass

**Step 3: Verify no regressions**

Confirm all existing tests still pass after changes.

---

## Summary

| Task | Description | Files |
|------|-------------|-------|
| 1 | Add SDK smoke tests to lead-enricher | `test_enrich.py` |
| 2 | Add SDK smoke tests to distributor-inspector | `test_search.py` |
| 3 | Create pyproject.toml for lead-enricher | `pyproject.toml` (new) |
| 4 | Create pyproject.toml for distributor-inspector | `pyproject.toml` (new) |
| 5 | Create pyproject.toml for shared | `pyproject.toml` (new) |
| 6 | Delete old requirements.txt | `requirements.txt` (delete) |
| 7 | Update SKILL.md docs | `SKILL.md` (modify) |
| 8 | Run all tests | Verify |
