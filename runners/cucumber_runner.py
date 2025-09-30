"""
BDD Cucumber Runner using Behave
"""
from behave import __main__ as behave_main
import sys
import os
import logging


class CucumberRunner:
    """Runner for BDD tests using Behave"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def run_features(self, features_path="features", tags=None):
        """Run BDD features"""
        self.logger.info("Running BDD features...")

        args = [
            features_path,
            "--format=allure_behave.formatter:AllureFormatter",
            "-o", "reports/allure/allure-results",
            "--format=json",
            "-o", "reports/cucumber/cucumber-report.json"
        ]

        if tags:
            args.extend(["--tags", tags])

        sys.argv = ["behave"] + args
        behave_main.main()
