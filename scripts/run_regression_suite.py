import glob
import subprocess
import sys

files = sorted(
    glob.glob("tests/test_phase4*.py")
    + glob.glob("tests/test_phase5*.py")
    + glob.glob("tests/test_phase6*.py")
)
cmd = [sys.executable, "-m", "pytest"] + files
print(f"Executing: {' '.join(cmd)}")
res = subprocess.run(cmd)
sys.exit(res.returncode)
