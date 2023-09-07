# Python Unittest Auto-Discovery Issue

This code demonstrates an issue I noticed with Python's `unittest` module when running tests programmatically via a
subprocess (e.g. `subprocess.Popen()`, `subprocess.run()`, `asyncio.create_subprocess_exec()`).

See also: https://stackoverflow.com/questions/77061446/why-does-python-unittest-auto-discovery-not-work-when-running-in-a-subprocess

## Expected Behavior

When running tests from the command line, Python's `unittest` module auto-discovers tests in the `test` directory:

```shell
python -m unittest discover test '*_test.py' --locals -bcf
....
----------------------------------------------------------------------
Ran 4 tests in 0.855s

OK
```

## Actual Behavior

...but it fails to auto-discover tests when that same command is run using Python's `subprocess` module:

```shell
$ python -m src.example.runner

Running tests using asyncio.run...

----------------------------------------------------------------------
Ran 0 tests in 0.000s

OK

Running tests using subprocess.Popen...

----------------------------------------------------------------------
Ran 0 tests in 0.000s

OK

Running tests using subprocess.run...

----------------------------------------------------------------------
Ran 0 tests in 0.000s

OK

Running tests using unittest.defaultTestLoader...

test_async_call (example.runner_test.AsyncTestRunner.test_async_call) ... ok
test_popen (example.runner_test.TestRunners.test_popen) ... ok
test_run (example.runner_test.TestRunners.test_run) ... ok
test_unittest_discover (example.runner_test.TestRunners.test_unittest_discover) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.864s

OK
```

Note that the `unittest.defaultTestLoader` test runner works as expected, because it is explicitly using the `unittest`
module to run the other tests. However, when running tests using `asyncio.run`, `subprocess.Popen`, or `subprocess.run`,
as if using the CLI from the command line, the tests are not auto-discovered.

## Different Python Versions

If you have Docker installed, you can run the tests in a container using any version of Python you like.  For example:

### Python 3.11 on Alpine Linux

```shell
docker run -it --rm -v $(pwd):$(pwd) -w $(pwd) --name test python:3.11-alpine python3 -m src.example.runner
```

### Python 3.10 on Ubuntu Linux

```shell
docker run -it --rm -v $(pwd):$(pwd) -w $(pwd) --name test python:3.10 python3 -m src.example.runner
```
