# AGENTS.md

## Project

Playwright + pytest UI automation framework targeting SauceDemo (https://www.saucedemo.com/).
Page Object Model. Author is transitioning from functional QA to Python automation;
code quality feedback is the point of this repo.

## Interaction Style

- When the user asks something, answer and explain — don't fix-and-stop. Explain the
  reasoning, the trade-offs, and what was changed and why.
- Only act when asked. "Just do it" (or equivalent) means skip the explanation and make
  the change directly.

## Structure

- `po/` — page objects and components
- `tests/` — test suites and conftest with shared fixtures
- `data/` — test data constants
- `conftest.py` — shared fixtures: page setup, login, inventory/cart/checkout state presets

## Commands

```bash
pip install -r requirements.txt   # install project dependencies (create from .venv: pip freeze > requirements.txt)
playwright install                # download browser binaries (Chromium/Firefox) needed to run tests
pytest                            # run the test suite
allure open                       # view the generated Allure report (requires the allure CLI: npm install -g allure)
black .                           # format the codebase
```

## Reports

- `report.html` — quick report (pytest-html, self-contained). Generated automatically
  on every run; single-run view of passed/failed tests with logs, no cross-run data.
  Open it directly in a browser.
- Allure — historical report with trends, run manually when you want it:

  ```bash
  pytest                          # results are collected into allure-results/ on every run
  rm -rf allure-report            # required — Allure 3 never overwrites an existing report
  allure generate allure-results  # build the static report (Allure 3, reads allurerc.json)
  allure open                     # serve it in the browser
  ```

  History is stored in a single JSONL file (`allure/history.jsonl`, set via
  `historyPath` in `allurerc.json`) that Allure appends to on every generation — no
  manual copying; capped at 20 runs (`historyLimit`). Requires the allure CLI
  (`npm install -g allure`).
  Warning: if `allure-report/` already contains a report, `allure generate` does not
  overwrite it — it silently writes the new report into a nested `allure-report/awesome/`
  and exits 0, so the browser keeps showing the old report (looks "stuck"). Always
  delete the output directory first; `allure/history.jsonl` is safe (it lives outside
  the report directory).

## Conventions

- Page objects expose behaviour, not locators. No assertions inside `po/`.
- Locators: prefer `get_by_role` / `get_by_label` / `get_by_test_id` over CSS or XPath.
- No fixed sleeps. Rely on Playwright auto-waiting.
- Tests must be independent and order-agnostic.
- **Test naming:** `test_<descriptive_snake_case>` — no numbered prefixes (tests are order-agnostic). Omit `test_` number prefixes on new tests; migrate away from them over time.
- **Fixture naming:** `<state>_<page>` for default/empty states (e.g., `empty_cart_page`), `<page>_with_<state>` for pre-loaded states (e.g., `cart_page_with_item`). Test-local fixtures use imperative verbs (e.g., `ensure_no_errors`).

## Review Criteria

Priority order — go for the top of this list first.

### Test & framework design

- Coupling between page objects; Playwright internals leaking into tests
- Assertions in page objects instead of tests
- Test interdependence; shared mutable state; missing cleanup
- Premature abstraction, and duplication that should be extracted
- Whether a helper belongs as a method, a fixture, or a module function

### pytest

- Fixture scope (function/class/session) and the cost of getting it wrong
- Fixtures doing too much, or hiding setup the reader needs to see
- Parametrization that obscures intent; unreadable failure IDs
- `conftest.py` turning into a dumping ground

### Playwright

- Brittle locators tied to DOM structure
- Any fixed sleep or manual wait
- Sources of flakiness; whether a failure is diagnosable from output alone
- Trace/screenshot/video on failure

### Python craft

- Naming that doesn't say what the thing is
- Broad `except`; swallowed exceptions; mutable default arguments
- Type hints where they prevent a real error
- Non-idiomatic code where a standard-library option is clearer

### Production readiness

- Does it run in CI? Does it survive `pytest-xdist`?
- Hardcoded credentials, URLs, environments
- Could a stranger clone and run it from the README alone

## Review Behaviour

- No praise. Lead with the most serious issue, not the easiest to explain.
- One issue at a time. Name it, ask one question, stop.
- Label severity: design flaw / anti-pattern / style.
- "Works" is not the bar. If a senior engineer would reject it in review, say so.
