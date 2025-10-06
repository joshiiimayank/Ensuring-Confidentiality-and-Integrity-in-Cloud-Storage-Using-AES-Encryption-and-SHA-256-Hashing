import os

def discover_files(base_dir):
    file_list = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            file_list.append(os.path.relpath(os.path.join(root, file), base_dir))
    return file_list
