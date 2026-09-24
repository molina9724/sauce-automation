## To Do

* [ ] Implement a web page like documentation
* [ ] Implement a series of global test cases for left menu and its components in the pages it's displayed
* [ ] Add Docstrings to every method and function
* [ ] Add type hint to all constants and variables
* [ ] Add return type annotations to all the methods and functions
* [ ] Add parameter annotations to all the classes, methods and functions
* [ ] Add test cases to `test_checkout_step_2`
* [ ] Fixture set grew combinatorially; needs a factory
* [ ] Investigate centralized fixture parametrization ("fixture matrix") for
  shared test cases across page states; compare parametrized fixtures, indirect
  parametrization, and `pytest_generate_tests`
* [ ] Add repeated-purchase coverage for one, two, and three completed purchases
  without including login tests in that workflow matrix

## Done

* [X] Implement the test cases for `test_inventory_item`
* [X] Make page public
* [X] Login once per worker through the UI, reused via `storage_state`
* [X] Failure artifacts: trace, screenshot, video
* [X] Allure or HTML reporting (both of them are implemented)
* [X] GitHub Actions workflow running the suite on push
* [X] Cross-browser parametrization via pytest.ini (disabled by default because of performance)
* [X] Implement `checkout_complete`
