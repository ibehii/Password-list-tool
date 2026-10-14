"""Static code verification tests to enforce project coding standards."""

from __future__ import annotations

import ast
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_no_single_char_i_or_j_variables() -> None:
    """Verify that neither 'i' nor 'j' is used as a variable name anywhere in the codebase."""
    python_files: list[Path] = []
    for dir_path in [PROJECT_ROOT / "lib", PROJECT_ROOT / "tests", PROJECT_ROOT]:
        if dir_path.is_dir():
            for entry_file in dir_path.glob("*.py"):
                python_files.append(entry_file)

    forbidden_identifiers = {"i", "j"}
    violations: list[str] = []

    for source_file in python_files:
        file_content = source_file.read_text(encoding="utf-8")
        parsed_ast = ast.parse(file_content, filename=str(source_file))

        for ast_node in ast.walk(parsed_ast):
            # Check variable assignments and names
            if isinstance(ast_node, ast.Name) and ast_node.id in forbidden_identifiers:
                violations.append(
                    f"{source_file.name}:{getattr(ast_node, 'lineno', '?')} -> variable name '{ast_node.id}'"
                )
            # Check function arguments
            elif isinstance(ast_node, ast.arg) and ast_node.arg in forbidden_identifiers:
                violations.append(
                    f"{source_file.name}:{getattr(ast_node, 'lineno', '?')} -> argument name '{ast_node.arg}'"
                )
            # Check function / class names
            elif isinstance(ast_node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and ast_node.name in forbidden_identifiers:
                violations.append(
                    f"{source_file.name}:{getattr(ast_node, 'lineno', '?')} -> definition name '{ast_node.name}'"
                )

    error_message = "\n".join(violations)
    assert not violations, f"Found forbidden single-letter variable names ('i' or 'j'):\n{error_message}"
