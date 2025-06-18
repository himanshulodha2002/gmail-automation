"""Nox configuration for automated testing and linting."""

import nox

nox.options.sessions = ["lint", "type-check", "test"]
nox.options.reuse_existing_virtualenvs = True

PYTHON_VERSIONS = ["3.11"]
PACKAGE = "gmail_automation"
PACKAGE_PATH = f"src/{PACKAGE}"


@nox.session(python=PYTHON_VERSIONS)
def lint(session: nox.Session) -> None:
    """Run ruff linting and formatting."""
    session.install("ruff")
    session.run("ruff", "format", ".", "--check")
    session.run("ruff", "check", ".")


@nox.session(python=PYTHON_VERSIONS)
def format(session: nox.Session) -> None:
    """Format code with ruff."""
    session.install("ruff")
    session.run("ruff", "format", ".")
    session.run("ruff", "check", ".", "--fix")


@nox.session(python=PYTHON_VERSIONS)
def type_check(session: nox.Session) -> None:
    """Run mypy type checking."""
    session.install("mypy", "types-python-dateutil", "types-pytz")
    session.install("-e", ".[dev]")
    session.run("mypy", PACKAGE_PATH, "tests")


@nox.session(python=PYTHON_VERSIONS)
def test(session: nox.Session) -> None:
    """Run unit tests with pytest."""
    session.install("-e", ".[test]")
    session.run(
        "pytest",
        "tests/unit",
        "-v",
        "--cov",
        "--cov-report=term-missing",
        "--cov-report=html",
        *session.posargs,
    )


@nox.session(python=PYTHON_VERSIONS)
def test_integration(session: nox.Session) -> None:
    """Run integration tests."""
    session.install("-e", ".[test]")
    session.run(
        "pytest",
        "tests/integration",
        "-v",
        "-m",
        "integration",
        *session.posargs,
    )


@nox.session(python=PYTHON_VERSIONS)
def test_all(session: nox.Session) -> None:
    """Run all tests."""
    session.install("-e", ".[test]")
    session.run(
        "pytest",
        "-v",
        "--cov",
        "--cov-report=term-missing",
        "--cov-report=html",
        *session.posargs,
    )


@nox.session(python=PYTHON_VERSIONS)
def docs(session: nox.Session) -> None:
    """Build documentation."""
    session.install("-e", ".[dev]")
    session.install("sphinx", "sphinx-rtd-theme")
    session.run("sphinx-build", "-b", "html", "docs", "docs/_build/html")


@nox.session(python=PYTHON_VERSIONS)
def pre_commit(session: nox.Session) -> None:
    """Run pre-commit hooks."""
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files")


@nox.session(python=PYTHON_VERSIONS)
def safety(session: nox.Session) -> None:
    """Check dependencies for security vulnerabilities."""
    session.install("safety")
    session.install("-e", ".")
    session.run("safety", "check")
