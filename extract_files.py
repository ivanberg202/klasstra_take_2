import os

def get_files_as_project_structure(base_folder, output_file):
    excluded_dirs = {"node_modules", "env", "migrations", "__pycache__"}
    excluded_files = {"alembic.ini", "cleanup_script.py", "extract_files.py", "setup_script.py", "package-lock.json", "project_structure.py"}

    project_structure = {}

    for root, dirs, files in os.walk(base_folder):
        # Exclude hidden directories and specific excluded ones
        dirs[:] = [d for d in dirs if d not in excluded_dirs and not d.startswith(".")]

        for file in files:
            # Exclude hidden files, specific excluded files, and pycache files
            if file in excluded_files or file.startswith(".") or "__pycache__" in file:
                continue

            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, base_folder)

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Escape content for single-line representation
                    single_line_content = f"# filename: {relative_path}\\n" + repr(content)
                    project_structure[relative_path] = single_line_content
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")

    # Write the project structure to the output file
    with open(output_file, 'w', encoding='utf-8') as out_file:
        out_file.write("project_structure = {\n")
        for path, content in project_structure.items():
            out_file.write(f'  "{path}": {content},\n')
        out_file.write("}\n")

    print(f"Project structure successfully written to {output_file}")

if __name__ == "__main__":
    # Change these paths as needed
    base_folder = "."  # Use current directory as base folder
    output_file = "project_structure.py"  # Output Python script

    get_files_as_project_structure(base_folder, output_file)
