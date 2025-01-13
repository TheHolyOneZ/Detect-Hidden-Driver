"""
==============================================
    TheZ Hidden Drive Detector and Cleaner
    Version: 1.4
    Updated: 13.01.2025
    Contact: https://discord.gg/zsGTqgnsmK
==============================================
"""

import os
import subprocess
import shutil
from datetime import datetime

# === CONFIGURATION ===
LOG_DIR_NAME = "HiddenDriveLogs"
RECOVERY_DIR_NAME = "Recovery"
PROTECTED_DRIVES = ["C:"]  # Protect system drives by default


def display_watermark():
    """Display a watermark at the beginning of the script."""
    print("=" * 50)
    print("  TheZ Hidden Drive Detector and Cleaner")
    print("  Version: 1.4")
    print("  Updated: 13.01.2025")
    print("  Contact: https://discord.gg/zsGTqgnsmK")
    print("=" * 50)


def create_directory(path):
    """Ensure a directory exists."""
    if not os.path.exists(path):
        os.makedirs(path)


def create_log_directory():
    """Create a default or custom log directory."""
    default_log_dir = os.path.join(os.getcwd(), LOG_DIR_NAME)
    print(f"Default log directory: {default_log_dir}")
    use_custom = input("Do you want to use a custom log directory? (yes/no): ").strip().lower()

    if use_custom == 'yes':
        custom_dir = input("Enter the folder name or full path for logs: ").strip()
        log_dir = os.path.abspath(custom_dir)
    else:
        log_dir = default_log_dir

    create_directory(log_dir)
    return log_dir


def log_action(log_dir, message):
    """Log actions to a file with a timestamp in the specified directory."""
    log_file = os.path.join(log_dir, "hidden_drive_log.txt")
    with open(log_file, "a") as file:
        file.write(f"{datetime.now()} - {message}\n")


def get_all_drives():
    """Retrieve all drives (including hidden) using 'wmic logicaldisk get name'."""
    try:
        result = subprocess.run(['wmic', 'logicaldisk', 'get', 'name'],
                                stdout=subprocess.PIPE, text=True, shell=True)
        drives = [line.strip() for line in result.stdout.split('\n') if line.strip()]
        return drives[1:]  # Exclude the header
    except Exception as e:
        return []


def get_visible_drives():
    """Get drives visible to the Explorer."""
    try:
        visible_drives = [f"{chr(i)}:\\" for i in range(65, 91) if os.path.exists(f"{chr(i)}:\\")]
        return visible_drives
    except Exception as e:
        return []


def check_hidden_drives(all_drives, visible_drives):
    """Identify hidden drives by comparing all drives with visible drives."""
    hidden_drives = set(all_drives) - set(visible_drives)
    return list(hidden_drives)


def get_drive_details(drive):
    """Retrieve additional details about a drive using 'wmic'."""
    try:
        result = subprocess.run(['wmic', 'logicaldisk', 'where', f"name='{drive}'", 'get', 'caption,description,filesystem'],
                                stdout=subprocess.PIPE, text=True, shell=True)
        details = [line.strip() for line in result.stdout.split('\n') if line.strip()]
        return details[1:]  # Exclude the header
    except Exception as e:
        return []


def log_active_processes(drive, log_dir):
    """Log active processes using the drive."""
    try:
        result = subprocess.run(['wmic', 'process', 'where', f"ExecutablePath like '{drive}%'"],
                                stdout=subprocess.PIPE, text=True, shell=True)
        log_file = os.path.join(log_dir, "active_processes_log.txt")
        with open(log_file, "a") as file:
            file.write(f"{datetime.now()} - Processes using {drive}:\n")
            file.write(result.stdout)
        print(f"Active processes using {drive} logged.")
    except Exception as e:
        log_action(log_dir, f"Failed to log active processes for {drive}: {e}")


def confirm_action(prompt):
    """Ask the user for confirmation and return True if the user confirms."""
    while True:
        response = input(f"{prompt} (yes/no): ").strip().lower()
        if response in ['yes', 'no']:
            return response == 'yes'


def list_hidden_drives(hidden_drives):
    """List hidden drives and allow the user to select one by index or name."""
    print("\nSelect a drive to act upon:")
    for i, drive in enumerate(hidden_drives, start=1):
        print(f"{i}. {drive}")
    choice = input("Enter the number or drive letter (e.g., 1 or C:): ").strip()
    if choice.isdigit():
        return hidden_drives[int(choice) - 1]
    return choice if choice in hidden_drives else None


def move_drive_content_to_recovery(drive, recovery_dir, log_dir):
    """Move all content from the drive to a recovery folder instead of deleting it."""
    try:
        create_directory(recovery_dir)
        drive_path = drive + '\\'
        if os.path.exists(drive_path):
            moved_files = []
            log_action(log_dir, f"Moving all content from {drive} to recovery...")
            for item in os.listdir(drive_path):
                src = os.path.join(drive_path, item)
                dest = os.path.join(recovery_dir, item)
                shutil.move(src, dest)
                moved_files.append(dest)
            log_action(log_dir, f"Moved files:\n" + "\n".join(moved_files))
        else:
            log_action(log_dir, f"Drive {drive} does not exist or is already empty.")
    except Exception as e:
        log_action(log_dir, f"Error while moving content from {drive}: {e}")


def main():
    display_watermark()
    log_dir = create_log_directory()
    recovery_dir = os.path.join(log_dir, RECOVERY_DIR_NAME)
    log_action(log_dir, "Scanning for hidden drives...")
    
    # Step 1: Get all drives
    all_drives = get_all_drives()
    visible_drives = get_visible_drives()
    hidden_drives = check_hidden_drives(all_drives, visible_drives)
    
    # Exclude protected drives
    hidden_drives = [drive for drive in hidden_drives if drive not in PROTECTED_DRIVES]
    
    if not hidden_drives:
        log_action(log_dir, "No hidden drives detected.")
        print("No hidden drives detected.")
        return
    
    log_action(log_dir, f"Hidden Drives Detected: {hidden_drives}")
    print(f"Hidden Drives Detected: {hidden_drives}\n")
    
    # Step 2: Display details for hidden drives
    for drive in hidden_drives:
        print(f"Details for hidden drive {drive}:")
        details = get_drive_details(drive)
        for detail in details:
            print(f"  {detail}")
            log_action(log_dir, f"{drive} - {detail}")
        print("-" * 30)

        # Log active processes
        log_active_processes(drive, log_dir)

    # Step 3: Confirm unauthorized drives
    if not confirm_action("Do you know these drives are not supposed to be on your PC?"):
        selected_drive = list_hidden_drives(hidden_drives)
        if selected_drive:
            print(f"You selected drive: {selected_drive}")
            if confirm_action(f"Are you sure you want to move all content from {selected_drive} to recovery?"):
                move_drive_content_to_recovery(selected_drive, recovery_dir, log_dir)

                # Recheck after the action
                updated_hidden_drives = check_hidden_drives(get_all_drives(), get_visible_drives())
                if selected_drive in updated_hidden_drives:
                    log_action(log_dir, f"Drive {selected_drive} still detected after action.")
                    print(f"WARNING: Drive {selected_drive} is still present.")
                else:
                    log_action(log_dir, f"Drive {selected_drive} successfully cleared.")
                    print(f"Drive {selected_drive} has been successfully cleared.")
            else:
                print("Action aborted. No changes were made.")
                log_action(log_dir, "Action aborted by the user.")
    else:
        print("No unauthorized drives detected. No action required.")
        log_action(log_dir, "No unauthorized drives detected. No action required.")


if __name__ == "__main__":
    main()
