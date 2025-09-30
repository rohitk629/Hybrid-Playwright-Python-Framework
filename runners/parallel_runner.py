"""
Parallel Test Runner
"""
import pytest
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import logging


class ParallelTestRunner:
    """Runner for parallel test execution"""

    def __init__(self, max_workers=4):
        self.max_workers = max_workers
        self.logger = logging.getLogger(__name__)

    def run_parallel_pytest(self, test_path, markers=None):
        """Run pytest tests in parallel"""
        self.logger.info(f"Running tests in parallel with {self.max_workers} workers")

        args = [
            test_path,
            "-n", str(self.max_workers),
            f"--alluredir=reports/allure/allure-results",
            "-v"
        ]

        if markers:
            args.extend(["-m", markers])

        return pytest.main(args)

    def run_with_threading(self, test_suites):
        """Run multiple test suites in parallel using threading"""
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            for suite in test_suites:
                future = executor.submit(self._execute_suite, suite)
                futures.append(future)

            results = [future.result() for future in futures]

        return results

    def _execute_suite(self, suite_config):
        """Execute a test suite"""
        self.logger.info(f"Executing suite: {suite_config['name']}")
        return pytest.main(suite_config['args'])