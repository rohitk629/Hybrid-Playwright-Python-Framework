"""
Main Test Runner
"""
import pytest
import sys
import os
from datetime import datetime
import logging


class TestRunner:
    """Main test runner for executing tests"""

    def __init__(self):
        self.logger = self._setup_logger()
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def _setup_logger(self):
        """Setup logger"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)

    def run_all_tests(self, parallel=False, workers=4):
        """Run all tests"""
        self.logger.info("Starting test execution...")

        args = [
            "src/test",
            f"--alluredir=reports/allure/allure-results",
            "--html=reports/pytest/pytest-report.html",
            "--self-contained-html",
            "-v",
            "-s"
        ]

        if parallel:
            args.extend(["-n", str(workers)])

        exit_code = pytest.main(args)
        self._generate_reports()

        return exit_code

    def run_ui_tests(self, parallel=False, workers=4):
        """Run UI tests only"""
        self.logger.info("Starting UI test execution...")

        args = [
            "tests/ui",
            "-m", "ui",
            f"--alluredir=reports/allure/allure-results",
            "--html=reports/pytest/ui-tests-report.html",
            "--self-contained-html",
            "-v"
        ]

        if parallel:
            args.extend(["-n", str(workers)])

        return pytest.main(args)

    def run_api_tests(self, parallel=False, workers=4):
        """Run API tests only"""
        self.logger.info("Starting API test execution...")

        args = [
            "tests/api",
            "-m", "api",
            f"--alluredir=reports/allure/allure-results",
            "--html=reports/pytest/api-tests-report.html",
            "--self-contained-html",
            "-v"
        ]

        if parallel:
            args.extend(["-n", str(workers)])

        return pytest.main(args)

    def run_smoke_tests(self):
        """Run smoke tests"""
        self.logger.info("Starting smoke test execution...")

        args = [
            "src/test",
            "-m", "smoke",
            f"--alluredir=reports/allure/allure-results",
            "-v"
        ]

        return pytest.main(args)

    def run_regression_tests(self, parallel=True, workers=8):
        """Run regression tests"""
        self.logger.info("Starting regression test execution...")

        args = [
            "src/test",
            "-m", "regression",
            f"--alluredir=reports/allure/allure-results",
            "-v"
        ]

        if parallel:
            args.extend(["-n", str(workers)])

        return pytest.main(args)

    def _generate_reports(self):
        """Generate Allure reports"""
        self.logger.info("Generating Allure reports...")
        os.system("allure generate reports/allure/allure-results -o reports/allure/allure-report --clean")