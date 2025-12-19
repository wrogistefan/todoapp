import subprocess

def test_main_runs():
    result = subprocess.run(
        ["python", "src/main.py"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
