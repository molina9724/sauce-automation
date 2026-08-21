# SauceDemo Automation Framework

![CI](https://github.com/molina9724/sauce-automation/actions/workflows/test.yml/badge.svg)

UI test automation for [saucedemo.com](https://www.saucedemo.com/), built with
Playwright and pytest using the Page Object Model.

Personal project built while transitioning from functional QA to Python test
automation. Actively developed — see [Known Limitations](#known-limitations).

## Highlights

- **80 tests** covering login, inventory, cart, checkout and navigation
- **Trace, video and screenshot captured on every failure** and uploaded as CI
  artifacts — a CI failure can be replayed locally in the Playwright trace viewer
- **Parallel execution** with per-worker authentication via `storage_state`
- **JUnit reporting** — failing tests are named inline in the GitHub Actions UI,
  not buried in logs
- **Protected `main`** — merges are blocked until CI passes
- Retrying assertions throughout; no fixed sleeps anywhere in the suite

## Stack

| Tool              | Purpose                                |
| ----------------- | -------------------------------------- |
| Python 3.10       | Language                               |
| Playwright        | Browser automation and assertions      |
| pytest            | Test runner, fixtures, parametrization |
| pytest-playwright | Browser fixtures, artifact capture     |
| pytest-xdist      | Parallel execution                     |
| pytest-timeout    | Per-test timeout ceiling               |
| pytest-html       | Self-contained HTML report             |
| allure-pytest     | Allure results                         |
| black             | Formatting                             |

CI runs on Python 3.12 since there's a package problem with 3.10.

## Quick Start

```bash
git clone https://github.com/molina9724/sauce-automation.git
cd sauce-automation
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
pytest
```

## Usage

```bash
pytest                       # full suite (parallel by default)
pytest -n 0                  # serial — use this when debugging
pytest tests/test_login.py   # single module
pytest --headed              # watch it run
pytest -m anonymous          # only tests that run logged out
pytest -k "cart"             # by keyword
```

Cross-browser runs are configured but disabled by default. See the commented
`--browser` line in `pytest.ini`.

### Investigating a failure

Failures produce a trace, video and screenshot under `test-results/`:

```bash
playwright show-trace test-results/*/trace.zip
```

The same artifacts are attached to failed CI runs, so a failure that only
reproduces on the runner can still be inspected locally.

## Structure

```
po/pages/          Page objects — locators, behaviour, navigation
po/components/     Shared components composed onto pages (Cart, Menu, FormValidation)
tests/             Test modules, one per feature area
tests/conftest.py  Fixtures: authentication, page-object composition
data/              Expected values and parametrization data
.github/workflows/ CI pipeline
```

## Design Decisions

**Page objects expose locators; tests own the assertions.**
Locators are public attributes. Tests assert with Playwright's `expect()`, which
retries and reports expected value, actual value, resolved locator and call log.
This follows Playwright's official Page Object Model guidance.

**No boolean-returning visibility methods.**
An `is_x_displayed() -> bool` discards every diagnostic the page object had; the
test fails with `assert False` and nothing else. `expect(locator).to_be_visible()`
gives a real failure message and retries.

**Playwright's `expect` is used directly in test files.**
It is the assertion library, in the same way pytest is the runner. The
abstraction being built is over the *application* — pages, flows, business
vocabulary — not over the browser driver.

**Actions are separated from outcomes.**
`submit_credentials()` performs an action and promises nothing.
`login()` promises success and fails loudly if it does not happen. Expected
application behaviour — a rejected login, an access-denied banner — is asserted
in the test, never raised as an exception.

**Native Playwright errors are not wrapped.**
They carry the call log, retry count and navigation history. Replacing them with
a hand-written message discards the most useful part.

**Expected values live in `data/`.**
Never compared against values read from the page under test.

**Locator strategy:** `get_by_role` and accessible names for interactive
elements; CSS for structural containers where the markup provides no accessible
handle.

**No fixed sleeps.** Playwright's auto-waiting and retrying assertions handle all
synchronisation.

## Continuous Integration

Runs on every push and pull request:

1. Restore pip and Playwright browser caches
2. `black --check`
3. Full suite, parallel, Chromium
4. Publish JUnit results as an annotated check
5. On failure, upload traces, videos, screenshots, HTML and Allure results

Concurrency cancels superseded runs on branches while preserving a verdict for
every commit on `main`. `main` is protected: pull requests are required and the
`build` check must pass before merging.

## Known Limitations

This suite does **not** currently do:

- **Authentication is hardcoded to `standard_user`.** Testing `problem_user`,
  `visual_user` or `error_user` requires a manual login in an `anonymous` test,
  which forfeits fixture composition
- **Checkout completion is not implemented** — `/checkout-complete.html` has no
  page object and the purchase flow is never finished
- **Image assertions verify visibility, not loading.** A broken `<img>` is still
  visible, so `problem_user`'s broken images would pass
- **Item selection is index-based**, coupling tests to the default sort order
- **Base URL is hardcoded**; no environment configuration layer
- **No linter or type checker in CI** — static analysis is editor-only
- **CI runs macOS and Chromium only**
- **Migration in progress:** `LoginPage` and `InventoryPage` use the current
  assertion patterns; `CartPage`, `CheckoutStepOnePage`, `CheckoutStepTwoPage`
  and the shared components still use the older wrapper-based approach

## Roadmap

- [ ] Finish migrating remaining page objects to public locators + `expect()`
- [ ] Implement the checkout-complete page and the full purchase flow
- [ ] Parametrise authentication by user to cover `problem_user` and friends
- [ ] Replace index-based item selection with name-based locators
- [ ] Environment configuration for base URL
- [ ] Add static analysis to CI
- [ ] Publish the Allure report

## Notes

`AGENTS.md` documents the project conventions and the code-review criteria this
repo is held to.
