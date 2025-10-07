"""
BDD Feature Runner using Behave
"""
from behave import __main__ as behave_main
import sys
import os
import logging


class FeatureRunner:
    """Runner for BDD feature tests using Behave"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def run_features(self, features_path="features", tags=None,
                     format_type="pretty", output_dir="reports/allure/allure-results"):
        """
        Run BDD features

        Args:
            features_path: Path to features directory
            tags: Tags to filter scenarios (e.g., '@smoke', '@api')
            format_type: Output format ('pretty', 'json', etc.)
            output_dir: Directory for reports
        """
        self.logger.info(f"Running BDD features from: {features_path}")

        # Create output directory
        os.makedirs(output_dir, exist_ok=True)

        # Build command arguments
        args = [
            features_path,
            "-f", "allure_behave.formatter:AllureFormatter",
            "-o", output_dir,
            "-f", format_type,
            "--no-capture"
        ]

        if tags:
            args.extend(["--tags", tags])

        # Run behave
        sys.argv = ["behave"] + args

        try:
            behave_main.main()
            self.logger.info("Feature execution completed")
        except SystemExit as e:
            if e.code == 0:
                self.logger.info("All features passed")
            else:
                self.logger.warning(f"Some features failed (exit code: {e.code})")
            return e.code

    def run_smoke_features(self):
        """Run smoke test features"""
        return self.run_features(tags="@smoke")

    def run_ui_features(self):
        """Run UI test features"""
        return self.run_features(features_path="features/ui", tags="@ui")

    def run_api_features(self):
        """Run API test features"""
        return self.run_features(features_path="features/api", tags="@api")


if __name__ == "__main__":
    runner = FeatureRunner()
    runner.run_features()