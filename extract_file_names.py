# File: project_structure_file_names.py
import os
import datetime  # For handling date and time

def get_file_names_as_project_structure(base_folder, output_file):
    excluded_dirs = {"node_modules", "env", "migrations", "__pycache__"}
    excluded_files = {"alembic.ini", "cleanup_script.py", "extract_files.py", "setup_script.py", "package-lock.json", "project_structure.py"}
    
    file_names = []

    for root, dirs, files in os.walk(base_folder):
        # Exclude hidden directories and specific excluded ones
        dirs[:] = [d for d in dirs if d not in excluded_dirs and not d.startswith(".")]

        for file in files:
            # Exclude hidden files, specific excluded files, and files in __pycache__
            if file in excluded_files or file.startswith(".") or "__pycache__" in file:
                continue

            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, base_folder)
            file_names.append(relative_path)

    # Get current date and time
    now = datetime.datetime.now()
    formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")

    # Write the list of file names to the output file with a timestamp
    with open(output_file, 'w', encoding='utf-8') as out_file:
        out_file.write(f"# Generated on {formatted_now}\n")
        out_file.write("file_names = [\n")
        for name in file_names:
            out_file.write(f'    "{name}",\n')
        out_file.write("]\n")

    print(f"File names successfully written to {output_file}")

if __name__ == "__main__":
    base_folder = "."  # Change as necessary (current directory is used here)
    output_file = "project_structure_file_names.py"  # Output file
    get_file_names_as_project_structure(base_folder, output_file)
