import ast
import os
from nbformat import read, write, NO_CONVERT
from nbformat.v4 import new_code_cell, new_markdown_cell
from datetime import datetime
now = datetime.now().strftime("%Y-%m-%d")

NOTEBOOK_PATH = "investment-research-agent.ipynb"
PROJECT_ROOT = "src"  # base folder for your module imports
OUTPUT_PATH = "final_temp.ipynb"

inlined_modules = set()

def find_module_path(module_str):
    rel_path = os.path.join(*module_str.split(".")) + ".py"
    print("Combining",rel_path)
    return rel_path if os.path.exists(rel_path) else None

def extract_imports(file_path):
    with open(file_path, "r") as f:
        tree = ast.parse(f.read(), filename=file_path)
    
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            module = getattr(node, 'module', None)
            if module and module.startswith("src."):
                module_path = find_module_path(module)
                if module_path and module_path not in inlined_modules:
                    imports.append((module, module_path))
    return imports

def inline_module(module_path, added=set()):
    if module_path in added:
        return []
    added.add(module_path)

    cells = []

    # Recursively inline dependencies
    for mod, dep_path in extract_imports(module_path):
        cells += inline_module(dep_path, added)

    # Add the module code itself
    with open(module_path, "r") as f:
        code = f.read()
    
    cells.append(new_markdown_cell(
        source=(
            f"---\n"
            f"### Inlined Code: `{module_path}`\n\n"
            f" - **Module path**: `{module_path.replace('/', '.').replace('.py', '')}`  \n"
            f" - **Reason**: This file was imported in the original notebook and has been inlined here "
            f"to assist with submitting only one notebook file.\n"
            f" - **Inlined on**: {now}\n"
        )
    ))

    cells.append(new_code_cell(
        source=code
    ))
    return cells

def flatten_notebook():
    with open(NOTEBOOK_PATH) as f:
        nb = read(f, NO_CONVERT)

    new_cells = []
    for cell in nb.cells:
        if cell.cell_type == "code":
            lines = cell.source.split("\n")
            for line in lines:
                if "from src." in line or "import src." in line:
                    print("found")
                    parts = line.replace("from ", "").replace("import ", "").split()
                    module = parts[0]
                    print(module)
                    path = find_module_path(module)
                    if path:
                        print("path", path)
                        print(f"Inlining {module} from {path}")
                        inlined_cells = inline_module(path)
                        new_cells.extend(inlined_cells)
            # Add original notebook cell after inlined dependencies
            new_cells.append(cell)
        else:
            new_cells.append(cell)

    nb.cells = new_cells
    with open(OUTPUT_PATH, "w") as f:
        write(nb, f)

    print(f"Flattened notebook saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    flatten_notebook()
