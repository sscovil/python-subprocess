import asyncio
import os
import shutil
import subprocess
import unittest
from subprocess import CompletedProcess, PIPE
from typing import Final, List

UNIT_TEST_CMD: Final[str] = "python -m unittest discover test *_test.py --locals -bcf"


def _parse_cmd(cmd: str) -> List[str]:
    """Parses a command string into a list of arguments, using the full path to the executable."""
    args: List[str] = cmd.split(" ")
    executable: str = args.pop(0) if " " in cmd else cmd
    full_exec_path: str = shutil.which(executable)
    return [full_exec_path, *args]


async def async_exec(cmd: str, *args, **kwargs) -> int:
    """Runs a command using asyncio.create_subprocess_exec() and logs the output."""
    cmd_args: List[str] = _parse_cmd(cmd)
    process = await asyncio.create_subprocess_exec(*cmd_args, stdout=PIPE, stderr=PIPE, *args, **kwargs)
    stdout, stderr = await process.communicate()
    if stdout:
        print(stdout.decode().strip())
    else:
        print(stderr.decode().strip())
    return process.returncode


def popen(cmd: str, *args, **kwargs) -> int:
    """Runs a command using subprocess.call() and logs the output."""
    cmd_args: List[str] = _parse_cmd(cmd)
    with subprocess.Popen(cmd_args, stdout=PIPE, stderr=PIPE, text=True, *args, **kwargs) as process:
        stdout, stderr = process.communicate()
        if stdout:
            print(stdout.strip())
        else:
            print(stderr.strip())
        return process.returncode


def run(cmd: str, *args, **kwargs) -> int:
    """Runs a command using subprocess.run() and logs the output."""
    cmd_args: List[str] = _parse_cmd(cmd)
    process: CompletedProcess = subprocess.run(cmd_args, stdout=PIPE, stderr=PIPE, check=True, *args, **kwargs)
    if process.stdout:
        print(process.stdout.decode().strip())
    else:
        print(process.stderr.decode().strip())
    return process.returncode


def unittest_discover() -> unittest.TestResult:
    """Runs all tests in the given directory that match the given pattern, and returns a TestResult object."""
    start_dir = os.path.join(os.getcwd(), "test")
    pattern = "*_test.py"
    tests = unittest.TextTestRunner(buffer=True, failfast=True, tb_locals=True, verbosity=2)
    results = tests.run(unittest.defaultTestLoader.discover(start_dir=start_dir, pattern=pattern))
    return results


def main():
    """Runs the example."""
    print("\nRunning tests using asyncio.create_subprocess_exec...\n")
    asyncio.run(async_exec(UNIT_TEST_CMD))

    print("\nRunning tests using subprocess.Popen...\n")
    popen(UNIT_TEST_CMD)

    print("\nRunning tests using subprocess.run...\n")
    run(UNIT_TEST_CMD)

    print("\nRunning tests using unittest.defaultTestLoader...\n")
    unittest_discover()


if __name__ == "__main__":
    main()
