"""Code reference generation."""

from pathlib import Path
import sys

import mkdocs_gen_files


root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root))

nav = mkdocs_gen_files.Nav()
src = root / "microservices"

print(f"Scanning directory: {src}")
print(f"Found {len(list(src.rglob('*.py')))} Python files")

for path in sorted(src.rglob("*.py")):
    print(f"Processing: {path}")
    module_path = path.relative_to(src).with_suffix("")
    doc_path = path.relative_to(src).with_suffix(".md")
    full_doc_path = Path("reference", doc_path)

    parts = tuple(module_path.parts)
    print(f"  Module parts: {parts}")

    if parts[-1] == "__init__":
        parts = parts[:-1]
        doc_path = doc_path.with_name("index.md")
        full_doc_path = Path("reference", doc_path)
        print(f"  __init__ file, adjusted to: {parts}")
    elif parts[-1] == "__main__":
        print(f"  Skipping __main__ file")
        continue
    
    if parts:
        nav[parts] = doc_path.as_posix()
        print(f"  Added to nav: {parts} -> {doc_path.as_posix()}")

        with mkdocs_gen_files.open(full_doc_path, "w") as fd:
            identifier = "microservices." + ".".join(parts)
            
            print(f"# {identifier}", file=fd)
            print(f"\nSource file: `{path.relative_to(root)}`", file=fd)
            print(f"\n## Source Code", file=fd)
            print(f"\n```python", file=fd)
            try:
                with open(path, 'r', encoding='utf-8') as source_file:
                    print(source_file.read(), file=fd)
            except Exception as e:
                print(f"Could not read source file: {e}", file=fd)
            print("```", file=fd)

        mkdocs_gen_files.set_edit_path(full_doc_path, path.relative_to(root))

print(f"Generated documentation pages: {len(nav._data)}")
print("Navigation structure:")
for key, value in nav._data.items():
    print(f"  {key} -> {value}")

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
