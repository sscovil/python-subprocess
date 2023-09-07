import unittest

from src.example.runner import async_exec, popen, run, unittest_discover


class AsyncTestRunner(unittest.IsolatedAsyncioTestCase):
    async def test_async_call(self):
        self.assertEqual(await async_exec("echo Hello"), 0)


class TestRunners(unittest.TestCase):
    def test_popen(self):
        self.assertEqual(popen("echo Hello"), 0)

    def test_run(self):
        self.assertEqual(run("echo Hello"), 0)

    def test_unittest_discover(self):
        results = unittest_discover()
        self.assertEqual(results.testsRun, 4)  # There are 4 test cases in this file


if __name__ == "__main__":
    unittest.main()
