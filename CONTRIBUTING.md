
# Contributing to Paystack Python Client

Thanks for your interest in contributing. Contributions, issues, and feature requests are welcome!

## Getting Started

1. **Fork the repository** and clone your fork:

   ```bash
   git clone https://github.com/<your-username>/paystack_client.git
   cd paystack_client
   ```

2. **Set up a virtual environment** (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use venv\Scripts\activate
   ```

3. **Install development dependencies:**

   ```bash
   pip install -e ".[dev]"
   ```

4. **Run tests to verify setup:**

   ```bash
   pytest
   ```

---

## Making Changes

* **Follow PEP 8** for Python style.
* Keep code **typed** (use type hints).
* Ensure **all tests pass** before opening a PR.
* Add/update **docstrings** for public methods/classes.
* If adding a new API resource, also update the **README** and **USAGE.md** with examples.

---

## Submitting a Pull Request

1. Create a feature branch:

   ```bash
   git checkout -b feature/my-feature
   ```
2. Commit your changes (write clear, descriptive commit messages).
3. Push to your fork:

   ```bash
   git push origin feature/my-feature
   ```
4. Open a Pull Request against the `main` branch.

---

## Running Tests and Linting

* **Tests:**

  ```bash
  pytest --cov=paystack_client
  ```
* **Lint & formatting (black + flake8):**

  ```bash
  black .
  flake8 .
  ```

---

## Reporting Issues

If you find a bug or have a feature request:

* Check the [issue tracker](https://github.com/theolujay/paystack_client/issues) first.
* If it’s new, open an issue with:

  * Steps to reproduce
  * Expected behavior
  * Actual behavior
  * Any relevant logs or screenshots

---

## Code of Conduct

Please note that this project follows a [Code of Conduct](./CODE_OF_CONDUCT.md). By participating, you agree to uphold it.

---

**Pro tip:** Start small (typos, docs, tests) if you’re new. It helps you get familiar with the repo before diving into larger changes.