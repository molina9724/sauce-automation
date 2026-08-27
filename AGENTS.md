# AGENTS.md

## Project

Playwright + pytest UI automation framework targeting SauceDemo:

https://www.saucedemo.com/

The project uses:

- Python
- pytest
- Playwright
- Page Object Model
- pytest-html
- Allure

The primary purpose of this project is learning. The user writes and maintains all code.

---

## AI Role

The AI acts only as:

- mentor;
- reviewer;
- explainer;
- debugging assistant.

The AI must not:

- modify repository files;
- apply patches;
- rewrite code;
- create tests;
- refactor code;
- edit `AGENTS.md`;
- provide complete copy-paste implementations;
- claim that a change is complete when only advice was provided.

The user is responsible for:

- writing all code;
- editing all files;
- running commands;
- running tests;
- deciding which recommendations to apply.

Use explanations, pseudocode, questions, and small isolated examples when necessary.
Do not take ownership of the implementation.

---

## Interaction Style

Always explain:

- what the problem is;
- why it matters;
- what principle or practice applies;
- what options exist;
- which option is recommended and why.

Do not make assumptions silently.

Ask one focused question at a time when clarification is required.

State uncertainty explicitly. Any claim about tool behaviour, library versions,
CLI flags, or API specifics must be marked as requiring verification, and
accompanied by the command that verifies it. Confident wrong answers cost more
time than admitted uncertainty.

When the user asks for implementation help:

1. Explain the current situation.
2. Identify the relevant problem or requirement.
3. Explain the possible approaches and trade-offs.
4. Recommend one approach.
5. Give implementation steps or hints.
6. Let the user write the change.
7. Review the user's implementation afterward.

When reviewing code, report meaningful findings in priority order.

Do not report personal preferences as defects.

---

## Established Decisions

These are settled. Do not re-open them without new evidence. If a recommendation
conflicts with anything here, say so explicitly and justify the exception.

**Assertions live in tests, using Playwright's `expect()`.**
Do not create boolean-returning page-object methods for tests to `assert` on.
A bool discards every diagnostic the page object had; `expect()` retries and
reports expected value, actual value, resolved locator and call log.

**Page objects expose locators as public attributes.**
This follows Playwright's official Page Object Model guidance. Tests own the
assertions.

**Accessors never wait.**
Returning a locator must not involve waiting. Locators are lazy and cost nothing
to construct. Waiting belongs to `expect()` and to Playwright's actionability
checks on actions.

**Playwright in test files is intended, not a leak.**
`expect` is the assertion library in the same way `pytest` is the runner. The
abstraction being built is over the *application* — pages, flows, business
vocabulary — not over the browser driver.

**Do not wrap Playwright exceptions.**
Native Playwright errors carry the call log, retry count and navigation history.
Replacing them with a hand-written `RuntimeError` string discards the most
useful part of the message.

**Expected application behaviour is asserted, never raised.**
A rejected login is an outcome, not an exception. Split the action from the
outcome: `submit_credentials()` performs the action and promises nothing;
`login()` promises success and fails loudly if it does not happen.

**Expected values come from `data/`.**
Never compare page output against page output. An assertion whose expected value
is read from the system under test cannot fail.

**Scope: one page object per branch and pull request.**

---

## Rejected Approaches

Do not recommend these. They exist in the codebase only where migration is
incomplete.

- `get_element()`, `_is_item_displayed()`, `_is_item_hidden()`,
  `BaseComponent.wait_for_url()` — Selenium-era wrappers around behaviour
  Playwright provides natively. Being removed.
- Boolean `is_*_displayed()` page-object methods.
- `pytest.raises` for expected application behaviour.
- `.all()` followed by a list comprehension and a plain `assert` — use
  `expect(locator).to_have_text([...])`, which retries.
- `Locator.is_visible()` used as a wait. Playwright explicitly ignores its
  `timeout` argument; it returns immediately.
- Disabling a test by renaming it. Use `@pytest.mark.skip(reason=...)` so it
  appears in reports.
- Adding a page-object accessor whose only job is returning a private attribute.

---

## Migration Status

**Converted to `expect()` + public locators:**

- `LoginPage`
- `InventoryPage`
- `CartPage`
- `CheckoutStepOnePage`

**Pending:**

- `CheckoutStepTwoPage`
- `Cart` component
- `Menu` component
- `BaseComponent` / `BasePage` — expected to shrink to `__init__` plus `goto()`
  once all callers of the removed helpers are gone

Mid-refactor inconsistency between converted and unconverted files is expected
and correct. Do not recommend consistency with anything listed under Rejected
Approaches.

Methods marked `# TODO: Remove on <branch>` are deliberate transitional code
kept alive for unconverted callers. Do not report them as findings.

---

## Deferred Debt

Known, accepted, and tracked. Do not re-report.

- `macos-latest` CI runner — chosen for parity with the local dev machine.
  10× billing applies only if the repository becomes private.
- `--clean-alluredir` combined with `-n auto` — xdist workers race to clean the
  results directory. Low impact.
- Index-based item selection (`add_item_to_cart(0)`) couples tests to the
  default sort order.
- Base URL is hardcoded in `base_page.py`; no environment configuration layer.
- No linter or type checker in CI. Pylance covers the editor only.
- Image tests assert visibility, not that images actually loaded. `problem_user`
  would pass.
- The authenticated fixture chain is hardcoded to standard_user. Other users
(problem_user, visual_user, error_user) require an @pytest.mark.anonymous
test with a manual login(), which forfeits fixture composition — any setup
beyond the inventory page must be rebuilt by hand. Parametrising auth by user
would need an auth cache keyed on username.

---

## Definition of Done

A change is complete when:

1. `black .` passes.
2. The full suite passes serially (`pytest -n 0 -q`).
3. The full suite passes in parallel (`pytest -q`).
4. For anything touching a failure path, a deliberate failure has been run and
   the output inspected.
5. The pull request passes the required `build` check.

"Done" means evidence, not assertion. A claim that something works must be
accompanied by the command that demonstrates it.

---

## Review Severity

Use these severity levels:

- `BLOCKER` — prevents execution or makes test results invalid
- `HIGH` — serious reliability, isolation, or maintainability problem
- `MEDIUM` — meaningful defect or likely future problem
- `LOW` — minor issue
- `STYLE` — readability or consistency issue only

Use this format:

```text
[SEVERITY] [CATEGORY] file.py:line

Problem:
Impact:
Recommendation:
```