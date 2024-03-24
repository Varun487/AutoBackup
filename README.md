# AutoBackup
An automated script to backup my computer's data into a hard drive.

## Functions

- Read default values and files to ignores from a json file
- Ask source and destination folder and whether to prompt before performing operations
- Build a dictionary with all destination file paths
    - Keys: File paths
    - Values: Operations (default `delete`)
- Walk through all paths in source, compare files with paths in dictionary and update operations for each path
    - Operations: `create`, `update`, `skip`
    - Ignore files mentioned in json
- Perform operations for each file path present in dictionary

## To run the script

1. Add your defaults and ignore files to the `temp_ignore.json` file
2. Rename `temp_ignore.json` to `ignore.json`
3. Run the script with the following command `python auto_backup.py`
