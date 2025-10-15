"""
Setup Configuration Script
Detects and fixes report location issues
"""
import subprocess
import os
import sys


def check_installed_plugins():
    """Check which pytest plugins are installed"""
    print("\n" + "="*70)
    print("Checking installed pytest plugins...")
    print("="*70)
    
    plugins_to_check = [
        'pytest-html',
        'pytest-json-report',
        'pytest-json',
        'allure-pytest'
    ]
    
    installed = []
    not_installed = []
    
    for plugin in plugins_to_check:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'show', plugin],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            installed.append(plugin)
            print(f"✓ {plugin} - INSTALLED")
        else:
            not_installed.append(plugin)
            print(f"✗ {plugin} - NOT INSTALLED")
    
    return installed, not_installed


def create_setup_cfg():
    """Create setup.cfg with proper report configurations"""
    setup_cfg_content = """[tool:pytest]
# Ensure all reports go to reports folder
addopts = 
    --html=reports/pytest/report.html
    --self-contained-html
    --json-report
    --json-report-file=reports/pytest/report.json
    --json-report-indent=2

# Prevent reports in root directory
htmlpath = reports/pytest/report.html
"""
    
    if not os.path.exists('setup.cfg'):
        with open('setup.cfg', 'w') as f:
            f.write(setup_cfg_content)
        print("\n✓ Created setup.cfg with proper report paths")
    else:
        print("\n⚠ setup.cfg already exists - please check manually")


def create_pyproject_toml():
    """Create pyproject.toml with proper report configurations"""
    pyproject_content = """[tool.pytest.ini_options]
# Ensure all reports go to reports folder
addopts = [
    "--html=reports/pytest/report.html",
    "--self-contained-html",
]

# JSON Report Configuration
json_report = "reports/pytest/report.json"
json_report_file = "reports/pytest/report.json"
json_report_indent = 2
"""
    
    if not os.path.exists('pyproject.toml'):
        with open('pyproject.toml', 'w') as f:
            f.write(pyproject_content)
        print("✓ Created pyproject.toml with proper report paths")
    else:
        print("⚠ pyproject.toml already exists - please check manually")


def create_pytest_ini():
    """Ensure pytest.ini has proper configuration"""
    print("\n✓ Use the updated pytest.ini provided")
    print("  Location: Replace your current pytest.ini with updated version")


def cleanup_root_reports():
    """Clean up any report files in root directory"""
    print("\n" + "="*70)
    print("Cleaning up misplaced report files...")
    print("="*70)
    
    root_report_files = [
        'pytest-html-report.html',
        'output.json',
        'report.json',
        'test-results.json',
        'results.json',
        'report.html'
    ]
    
    os.makedirs('reports/pytest', exist_ok=True)
    
    moved_files = []
    for filename in root_report_files:
        if os.path.exists(filename):
            target_path = f"reports/pytest/{filename}"
            try:
                if os.path.exists(target_path):
                    os.remove(target_path)
                os.rename(filename, target_path)
                moved_files.append(filename)
                print(f"✓ Moved {filename} to reports/pytest/")
            except Exception as e:
                print(f"✗ Could not move {filename}: {e}")
    
    if not moved_files:
        print("✓ No misplaced report files found in root directory")
    
    return moved_files


def create_directories():
    """Create required directory structure"""
    print("\n" + "="*70)
    print("Creating directory structure...")
    print("="*70)
    
    directories = [
        'reports/pytest',
        'reports/behave',
        'reports/allure/allure-results',
        'reports/allure/allure-report',
        'logs',
        'screenshots/failed'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created/verified: {directory}")


def show_configuration_tips(installed_plugins):
    """Show configuration tips based on installed plugins"""
    print("\n" + "="*70)
    print("CONFIGURATION RECOMMENDATIONS")
    print("="*70)
    
    if 'pytest-json-report' in installed_plugins or 'pytest-json' in installed_plugins:
        print("\n⚠ PYTEST-JSON-REPORT DETECTED")
        print("  This plugin creates 'output.json' by default.")
        print("  To fix this:")
        print("  1. Use the updated pytest.ini (includes json_report_file config)")
        print("  2. Or uninstall if not needed: pip uninstall pytest-json-report")
        print("  3. Or always use: pytest --json-report-file=reports/pytest/report.json")
    
    print("\n✅ RECOMMENDED CONFIGURATION:")
    print("  1. Replace pytest.ini with the updated version")
    print("  2. Replace conftest.py with the updated version")
    print("  3. Run: python setup_reports.py (this script)")
    print("  4. Test with: pytest --html=reports/pytest/report.html --self-contained-html")


def main():
    """Main setup function"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  PYTEST REPORT LOCATION SETUP & CLEANUP".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")
    
    # Check installed plugins
    installed, not_installed = check_installed_plugins()
    
    # Create directory structure
    create_directories()
    
    # Cleanup root directory
    moved_files = cleanup_root_reports()
    
    # Show configuration tips
    show_configuration_tips(installed)
    
    print("\n" + "="*70)
    print("NEXT STEPS")
    print("="*70)
    print("1. Replace pytest.ini with updated version")
    print("2. Replace conftest.py with updated version")
    print("3. Run tests: pytest --html=reports/pytest/report.html --self-contained-html")
    print("4. Verify report location: reports/pytest/report.html")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
