import subprocess

def test_cli_add():
    result = subprocess.run(
        ["python", "src/console_app.py", "add", "Test"],
        capture_output=True, text=True
    )
    assert "Test" in result.stdout

def test_cli_help():
    result = subprocess.run(
        ["python", "src/console_app.py"],
        capture_output=True, text=True
    )
    assert "Usage" in result.stdout or "help" in result.stdout.lower()
