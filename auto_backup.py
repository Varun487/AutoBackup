import os
import json
import shutil
import filecmp

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

def backup_data(source, destination, ignores, prompt=True):
    try:
        for root, _, files in os.walk(source):
            if not any((pattern in root) for pattern in ignores):
                folder_relative_path = os.path.relpath(root, source)
                folder_backup_path = os.path.join(destination, folder_relative_path)
                if not os.path.isdir(folder_backup_path):
                    os.mkdir(folder_backup_path)
                    print(f"Created directory {folder_relative_path}")                        
                for file in files:
                    if not any((pattern in file) for pattern in ignores):
                        file_source_path = os.path.join(root, file)
                        file_relative_path = os.path.relpath(file_source_path, source)
                        file_backup_path = os.path.join(destination, file_relative_path)
                        if os.path.exists(file_backup_path) and filecmp.cmp(file_source_path, file_backup_path):
                            print(f"Skipping {file_relative_path} (no changes)")
                        else:
                            if prompt:
                                permission = input(f"Copy {file_source_path}? (Y/n): ")
                                if not permission or permission == 'Y' or permission == 'y':
                                    shutil.copy2(file_source_path, file_backup_path)
                                    print(f"Copied {file_relative_path}")
                                else:
                                    print(f"Did not copy {file_relative_path}")
                            else:
                                shutil.copy2(file_source_path, file_backup_path)
                                print(f"Copied {file_relative_path}")
        print()
        print()
        print(f"Backup completed successfully to {destination}")
    except Exception as e:
        print(f"Error during backup: {e}")

def main():
    data = read_json_file('ignore.json')
    source = input_folders("Enter the path of the source folder", data['defaults']['source'])
    destination = input_folders("Enter the path of the destination folder", data['defaults']['destination'])
    prompt = input('Do you want to be prompted? (Y/n): ')
    if prompt == 'Y' or not prompt:
        prompt = True
    else:
        prompt = False
    backup_data(source, destination, data['ignore'], prompt)

if __name__ == "__main__":
    main()
