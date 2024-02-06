import ast
import sys


def remove_lines(lines, node, amount_removed=0):
    start_line = node.lineno - amount_removed
    end_line = node.end_lineno - amount_removed

    lines = lines[:start_line] + (lines[end_line + 1 :])
    amount_removed += end_line + 1 - start_line

    return lines, amount_removed


def remove_module_imports(code, modules_to_remove):
    syntax_tree = ast.parse(code)
    lines = code.splitlines()

    amount_removed = 1

    for node in syntax_tree.body:
        name = None
        if isinstance(node, ast.Import):
            name, *_ = node.names
        elif isinstance(node, ast.ImportFrom):
            name = node.module

        if name in modules_to_remove:
            lines, amount_removed = remove_lines(lines, node, amount_removed)

    return "\n".join(lines)


code = sys.stdin.read()
modules_to_remove = [
    "src.index",
    "src.package",
    "src.progressbar",
    "src.version",
    "src.sources_list",
    "src.file_manager",
    "src.install",
]

print(remove_module_imports(code, modules_to_remove))
