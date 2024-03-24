import os
import json
import shutil
import filecmp
import time

def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Unable to decode JSON in '{file_path}'.")
    except Exception as e:
        print(f"An unexpected error occurred {e}.")
    exit()

def input_folders(text, default):
    try:
        directory_path = input(f'{text} [{default}]: ')

        # If default is chosen
        if not directory_path:
            directory_path = default

        # Check if the entered path is a valid directory
        if not os.path.isdir(directory_path):
            raise NotADirectoryError(f'{directory_path} is not a directory or does not exist.')

        return directory_path

    except NotADirectoryError as e:
        print(f"Error: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    exit()

def build_file_path_operations(destination, ignores):
    # Build a dictionary with all destination file paths
    file_path_operations = {}
    for root, _, files in os.walk(destination):
        if not any((pattern in root) for pattern in ignores):
            for f in files:
                if not any((pattern in f) for pattern in ignores):
                    folder_relative_path = os.path.relpath(root, destination)
                    file_path_operations[os.path.join(folder_relative_path, f)] = 'delete'
    return file_path_operations

def update_file_path_operations(file_path_operations, source, destination, ignores):
    for root, _, files in os.walk(source):
        if not any((pattern in root) for pattern in ignores):
            folder_relative_path = os.path.relpath(root, source)
            for f in files:
                if not any((pattern in f) for pattern in ignores):
                    file_path = os.path.join(folder_relative_path, f)
                    if file_path not in file_path_operations:
                        file_path_operations[file_path] = 'create'
                    elif not filecmp.cmp(os.path.join(source, file_path), os.path.join(destination, file_path)):
                        file_path_operations[file_path] = 'update'
                    else:
                        file_path_operations[file_path] = 'skip'
    return file_path_operations

def perform_file_operation(operation, file_path, source, destination, permission):
    if not permission:
        print(f"Did not perform operation [{operation}] on {file_path}")
        return
    if operation == 'create' or operation == 'update':
        shutil.copy2(os.path.join(source, file_path), os.path.join(destination, file_path))
    elif operation == 'delete':
        os.remove(os.path.join(destination, file_path))
    print(f'[{operation}]: {file_path}')

def process_file_operations(file_path_operations, source, destination, prompt):
    progress = 0
    total = len(file_path_operations)
    for file_path in file_path_operations:
        permission = True
        if prompt and file_path_operations[file_path] != 'skip':
            permission = input(f"{file_path_operations[file_path]} {file_path}? (Y/n): ")
            permission = not permission or permission == 'Y' or permission == 'y' or permission.lower() == 'yes'
        perform_file_operation(file_path_operations[file_path], file_path, source, destination, permission)

def create_new_folders(source, destination, ignores, prompt):
    for root, _, files in os.walk(source):
        if not any((pattern in root) for pattern in ignores):
            folder_relative_path = os.path.relpath(root, source)
            folder_backup_path = os.path.join(destination, folder_relative_path)
            if not os.path.isdir(folder_backup_path):
                permission = True
                if prompt:
                    permission = input(f"create {folder_relative_path}? (Y/n): ")
                    permission = not permission or permission == 'Y' or permission == 'y' or permission.lower() == 'yes'
                if permission:
                    os.mkdir(folder_backup_path)
                    print(f'[create]: {folder_relative_path}')

def delete_empty_folders(source, destination, prompt):
    for root, _, files in os.walk(destination):
        folder_relative_path = os.path.relpath(root, destination)
        folder_source_path = os.path.join(source, folder_relative_path)
        if not len(os.listdir(root)) and not os.path.isdir(folder_source_path):
            permission = True
            if prompt:
                permission = input(f"delete {folder_relative_path}? (Y/n): ")
                permission = not permission or permission == 'Y' or permission == 'y' or permission.lower() == 'yes'
            if permission:
                os.rmdir(root)
                print(f'[delete]: {folder_relative_path}')

def backup_data(source, destination, ignores, prompt=False):
    try:
        print()
        print("Creating new folders:")
        print()

        # Create new folders
        create_new_folders(source, destination, ignores, prompt)

        print()
        print("Analyzing changes in files...")
        print()

        # Build a dictionary with all destination file paths
        file_path_operations = build_file_path_operations(destination, ignores)

        # Update file path operations by comparing with source files
        file_path_operations = update_file_path_operations(file_path_operations, source, destination, ignores)

        print()
        print("Processing file changes: ")
        print()

        # Process Dictionary
        process_file_operations(file_path_operations, source, destination, prompt)

        print()
        print("Deleting empty folders: ")
        print()

        # Delete empty folders
        delete_empty_folders(source, destination, prompt)

        print()
        print(f"Backup completed successfully to {destination}!")

    except Exception as e:
        print(f"Error during backup: {e}")

def main():
    # Read default values and files to ignores from a json file
    data = read_json_file('ignore.json')
    source = input_folders("Enter the path of the source folder", data['defaults']['source'])
    destination = input_folders("Enter the path of the destination folder", data['defaults']['destination'])
    prompt = input('Do you want to be prompted for changes? (y/N): ')
    prompt = prompt == 'y' or prompt == 'Y' or prompt.lower() == 'yes'
    
    # Run
    backup_data(source, destination, data['ignore'], prompt)

if __name__ == "__main__":
    main()
