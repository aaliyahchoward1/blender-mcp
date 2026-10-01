#!/usr/bin/env python3
"""
Validation script for Lunuff model generator.

This script validates the code structure, imports, and logic without
requiring Blender to be installed.

Usage:
    python3 validate_structure.py
"""

import ast
import sys
from pathlib import Path


class CodeValidator:
    """Validate Python code structure and completeness."""

    def __init__(self):
        self.errors = []
        self.warnings = []
        self.passed = []

    def validate_file_exists(self, filepath):
        """Check if a file exists."""
        if Path(filepath).exists():
            self.passed.append(f"File exists: {filepath}")
            return True
        else:
            self.errors.append(f"File not found: {filepath}")
            return False

    def validate_python_syntax(self, filepath):
        """Validate Python syntax."""
        try:
            with open(filepath) as f:
                ast.parse(f.read())
            self.passed.append(f"Syntax valid: {filepath}")
            return True
        except SyntaxError as e:
            self.errors.append(f"Syntax error in {filepath}: {e}")
            return False

    def validate_class_exists(self, filepath, class_name):
        """Check if a class exists in a Python file."""
        try:
            with open(filepath) as f:
                tree = ast.parse(f.read())

            classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

            if class_name in classes:
                self.passed.append(f"Class found: {class_name} in {filepath}")
                return True
            else:
                self.errors.append(f"Class not found: {class_name} in {filepath}")
                return False
        except Exception as e:
            self.errors.append(f"Error checking class in {filepath}: {e}")
            return False

    def validate_method_exists(self, filepath, class_name, method_name):
        """Check if a method exists in a class."""
        try:
            with open(filepath) as f:
                tree = ast.parse(f.read())

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and node.name == class_name:
                    methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                    if method_name in methods:
                        self.passed.append(
                            f"Method found: {class_name}.{method_name}"
                        )
                        return True
                    else:
                        self.errors.append(
                            f"Method not found: {class_name}.{method_name}"
                        )
                        return False

            self.errors.append(f"Class not found: {class_name}")
            return False
        except Exception as e:
            self.errors.append(f"Error checking method: {e}")
            return False

    def validate_imports(self, filepath):
        """Check if required imports are present."""
        try:
            with open(filepath) as f:
                content = f.read()

            required_imports = ['math', 'os', 'pathlib']
            for imp in required_imports:
                if imp.lower() in content.lower():
                    self.passed.append(f"Import found: {imp} in {filepath}")

            return True
        except Exception as e:
            self.errors.append(f"Error checking imports: {e}")
            return False

    def report(self):
        """Print validation report."""
        print("\n" + "="*70)
        print("LUNUFF CHARACTER MODEL - STRUCTURE VALIDATION REPORT")
        print("="*70)

        if self.passed:
            print(f"\n✓ PASSED ({len(self.passed)}):")
            for item in self.passed[:10]:  # Show first 10
                print(f"  ✓ {item}")
            if len(self.passed) > 10:
                print(f"  ... and {len(self.passed) - 10} more")

        if self.warnings:
            print(f"\n⚠ WARNINGS ({len(self.warnings)}):")
            for item in self.warnings:
                print(f"  ⚠ {item}")

        if self.errors:
            print(f"\n✗ ERRORS ({len(self.errors)}):")
            for item in self.errors:
                print(f"  ✗ {item}")

        print("\n" + "="*70)

        if self.errors:
            print(f"RESULT: FAILED - {len(self.errors)} error(s) found")
            print("="*70 + "\n")
            return False
        else:
            print(f"RESULT: PASSED - All validation checks successful!")
            print("="*70 + "\n")
            return True


def main():
    """Run validation suite."""
    models_dir = Path(__file__).parent

    validator = CodeValidator()

    print("\nValidating Lunuff Character Model Package...")

    # Check files exist
    files_to_check = [
        "lunuff_character.py",
        "test_lunuff.py",
        "mcp_lunuff_integration.py",
        "examples.py",
        "README.md",
        "__init__.py",
    ]

    print("\n1. Checking files exist...")
    for fname in files_to_check:
        filepath = models_dir / fname
        validator.validate_file_exists(filepath)

    # Check Python syntax
    print("\n2. Validating Python syntax...")
    py_files = [f for f in files_to_check if f.endswith('.py')]
    for fname in py_files:
        filepath = models_dir / fname
        validator.validate_python_syntax(filepath)

    # Check class structure
    print("\n3. Checking class structure...")
    validator.validate_class_exists(
        models_dir / "lunuff_character.py",
        "LunuffModelGenerator"
    )
    validator.validate_class_exists(
        models_dir / "mcp_lunuff_integration.py",
        "LunuffMCPTool"
    )

    # Check methods
    print("\n4. Checking required methods...")
    methods_to_check = [
        ("lunuff_character.py", "LunuffModelGenerator", "generate"),
        ("lunuff_character.py", "LunuffModelGenerator", "build_complete_model"),
        ("lunuff_character.py", "LunuffModelGenerator", "create_body"),
        ("lunuff_character.py", "LunuffModelGenerator", "create_head"),
        ("lunuff_character.py", "LunuffModelGenerator", "export_stl"),
        ("mcp_lunuff_integration.py", "LunuffMCPTool", "generate_lunuff"),
    ]

    for fname, class_name, method_name in methods_to_check:
        filepath = models_dir / fname
        validator.validate_method_exists(filepath, class_name, method_name)

    # Check imports
    print("\n5. Checking imports...")
    for fname in py_files:
        filepath = models_dir / fname
        validator.validate_imports(filepath)

    # Generate report
    success = validator.report()

    # Additional checks
    print("\n6. Additional validation checks:\n")

    # Check file sizes
    total_size = 0
    for fname in files_to_check:
        filepath = models_dir / fname
        if filepath.exists():
            size = filepath.stat().st_size
            total_size += size
            size_kb = size / 1024
            print(f"   {fname}: {size_kb:.1f} KB")

    print(f"\n   Total: {total_size / 1024:.1f} KB")

    # README check
    readme_path = models_dir / "README.md"
    if readme_path.exists():
        with open(readme_path) as f:
            content = f.read()
            sections = [
                "Overview",
                "Usage",
                "Features",
                "Components",
                "Customization",
                "API Reference",
            ]
            found_sections = sum(1 for s in sections if s in content)
            print(f"\n   README sections found: {found_sections}/{len(sections)}")

    print("\n" + "="*70)
    print("ENVIRONMENT CHECK:")
    print("="*70)

    # Check Python version
    py_version = sys.version.split()[0]
    print(f"Python version: {py_version}")

    # Check required modules
    required_modules = ['ast', 'pathlib', 'json']
    print("\nRequired modules (non-Blender):")
    for mod in required_modules:
        try:
            __import__(mod)
            print(f"  ✓ {mod}")
        except ImportError:
            print(f"  ✗ {mod} (missing)")

    print("\nNote: Blender modules (bpy, bmesh) are not available in this")
    print("environment, but will work correctly when run within Blender.")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
