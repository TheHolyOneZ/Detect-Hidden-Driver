# TheZ Hidden Drive Detector and Cleaner

**Version:** 1.5  
**Updated:** 13.01.2025  
**Contact:** [Discord Server](https://discord.gg/zsGTqgnsmK)

## Description
This script detects hidden drives on your system, identifies unauthorized ones, and allows you to take action by moving their contents to a recovery directory. It includes system drive protection, detailed logging, and active process monitoring.

## Features
- Detect hidden drives and retrieve their details.
- Log active processes using specific drives.
- Move hidden drive contents to a recovery folder instead of deleting them.
- Protect system drives from unintended actions.
- Automatically recheck if drives are removed after action.
- Detailed logging of all actions.

## Usage
1. Run the script. (exe or py)
2. Review the detected hidden drives.
3. Confirm if drives are unauthorized.
4. Select a drive to act upon.
5. Move contents to the recovery folder.
6. Check the logs folder for details!

## Configuration
- **Protected Drives:** Modify `PROTECTED_DRIVES` in the script to specify which drives should be excluded from actions.
- **Log Directory:** Default is `HiddenDriveLogs`. Customize during script execution.

## Logs
- All actions are logged in `hidden_drive_log.txt`.
- Active processes are logged in `active_processes_log.txt`.

## Recovery
Recovered files are moved to the `Recovery` directory under the log folder.

## Requirements
- Python 3.6+
- Windows OS

## Contact
For questions or support, join the [Discord Server](https://discord.gg/zsGTqgnsmK).
