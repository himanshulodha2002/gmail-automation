import nox

@nox.session(python=["3.9", "3.10", "3.11"])
def test(session):
    """Run unit tests."""
    session.install("pytest", "pytest-cov", "pytest-mock")
    session.install("-e", ".")
    session.run(
        "pytest", 
        "tests/unit", 
        "--cov=src/gmail_automation",
        "--cov-report=term-missing",
        "--cov-report=html",
        "--cov-fail-under=80",
        *session.posargs
    )

@nox.session
def test_integration(session):
    """Run integration tests."""
    session.install("pytest", "pytest-asyncio", "pytest-mock")
    session.install("-e", ".")
    session.run("pytest", "tests/integration", "-v", *session.posargs)

@nox.session
def lint(session):
    """Run linting with ruff."""
    session.install("ruff")
    session.run("ruff", "check", "src", "tests", "--fix")
    session.run("ruff", "format", "src", "tests")

@nox.session
def type_check(session):
    """Run type checking with mypy."""
    session.install("mypy", "types-PyYAML")
    session.install("-e", ".")
    session.run("mypy", "src/gmail_automation")

@nox.session
def security(session):
    """Run security checks with bandit."""
    session.install("bandit")
    session.run("bandit", "-r", "src/", "-f", "json", "-o", "bandit-report.json")