import os
import re

def build_preview():
    base_dir = "Codigo producido"
    index_path = os.path.join(base_dir, "Index.html")
    output_path = os.path.join(base_dir, "preview_local.html")
    
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    include_pattern = re.compile(r'<\?!=\s*include\(\s*[\'"]([^\'"]+)[\'"]\s*\)\s*;\s*\?>')

    def replace_include(match):
        filename = match.group(1) + ".html"
        filepath = os.path.join(base_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as inc_f:
                inc_content = inc_f.read()
                # Recursively replace nested includes (like in View_Home.html)
                return include_pattern.sub(replace_include, inc_content)
        else:
            print(f"Warning: File {filepath} not found for include.")
            return ""

    bundled = include_pattern.sub(replace_include, content)

    with open(output_path, "w", encoding="utf-8") as out_f:
        out_f.write(bundled)

    print(f"Successfully generated {output_path} ({len(bundled)} bytes)")

if __name__ == "__main__":
    build_preview()
