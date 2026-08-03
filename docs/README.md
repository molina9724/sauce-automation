# SauceDemo Automation Framework

UI test automation for [saucedemo.com] built with Playwright and pytest, using the
Page Object Model.

Personal project built while transitioning from functional QA to Python test
automation. Actively developed — see [Known Limitations](#known-limitations) for
current gaps.

## Stack

| Tool       | Purpose                                |
| ---------- | -------------------------------------- |
| Python 3.x |                                        |
| Playwright | Browser automation                     |
| pytest     | Test runner, fixtures, parametrization |
| black      | Formatting                             |

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
pytest                          # full suite
pytest tests/test_login.py      # single file
pytest --headed                 # watch it run
pytest -n auto                  # parallel
```

## Structure

```
po/          Page objects — behaviour, no assertions
tests/       Test suites, one module per feature
data/        Test data and fixtures
conftest.py  Shared fixtures: browser context, page, auth
```

## Design Decisions

- **Page objects expose behaviour, not locators.** Tests read as user actions;
  selectors never appear in test files.
- **No assertions in page objects.** Assertions belong to tests, so a page object
  stays reusable across tests with different expectations.
- **Role- and label-based locators** over CSS/XPath, so tests survive markup
  changes.
- **No fixed sleeps.** Playwright's auto-waiting handles synchronisation.
- **Validation logic extracted to `FormValidation`** rather than duplicated across
  login and checkout pages.

## Known Limitations

- [ ] No CI pipeline — tests run locally only
- [ ] Chromium only; Firefox and WebKit untested

## Roadmap

* [X] Allure or HTML reporting
* [X] Failure artifacts: trace, screenshot, video
* [ ] GitHub Actions workflow running the suite on push
* [ ] Cross-browser via parametrized fixtures

## Notes

`AGENTS.md` documents the project conventions and the code-review criteria I hold
this repo to.
