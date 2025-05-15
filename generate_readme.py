import os
from pathlib import Path

WATCHED_DIRS = ['archives']
README_PATH = 'README.md'
VALID_EXTENSIONS = {'.md'}

# def get_description(file_path):
#     try:
#         with open(file_path, 'r', encoding='utf-8') as f:
#             for line in f:
#                 if line.strip():
#                     return line.strip()[:100]
#     except:
#         return "No description available"
#     return "No description available"

def get_description(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if len(lines) >= 10:
                return lines[9].strip()[:100]  # 10th line (index 9)
            else:
                return "No description: less than 10 lines"
    except Exception as e:
        return f"Error reading file: {e}"


def build_file_tree():
    structure = {}
    for base in WATCHED_DIRS:
        for root, _, files in os.walk(base):
            md_files = [f for f in files if Path(f).suffix in VALID_EXTENSIONS]
            if md_files:
                rel_root = os.path.relpath(root)
                structure[rel_root] = []
                for f in md_files:
                    path = os.path.join(rel_root, f)
                    description = get_description(path)
                    structure[rel_root].append((f, path, description))
    return structure

def generate_readme_content():
    tree = build_file_tree()
    lines = [""]
    grouped = {}

    for path, files in tree.items():
        parts = path.split(os.sep)
        top = parts[0]
        sub = '/'.join(parts[1:]) if len(parts) > 1 else None
        grouped.setdefault(top, {}).setdefault(sub, []).extend(files)

    for top_folder, subfolders in grouped.items():
        lines.append(f"## {top_folder}")
        for subfolder, files in subfolders.items():
            if subfolder:
                lines.append(f"- **{subfolder}**")
            else:
                lines.append("- **(root)**")
            for filename, full_path, description in files:
                indent = "  "
                lines.append(f"{indent}- [{filename}]({full_path}): {description}")
        lines.append("")  # blank line
    return "\n".join(lines)

def update_readme():
    content = generate_readme_content()
    with open(README_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {README_PATH}")

if __name__ == "__main__":
    update_readme()
