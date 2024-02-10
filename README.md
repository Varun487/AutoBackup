# AutoBackup
An automated script to backup my computer's data into a hard drive.

## Functions

- Ask source and destination folder
- Notice changes in files and folders and prompt before updating backup folder
- Show overall backup progress and progress of copying current file or folder
- Read defaults and files to ignore from a json file

## To run the script

1. Add your defaults and ignore files to the `temp_ignore.json` file
2. Rename `temp_ignore.json` to `ignore.json`
3. Run the script with the following command `python auto_backup.py`
