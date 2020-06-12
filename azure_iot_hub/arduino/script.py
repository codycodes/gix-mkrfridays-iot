from pathlib import Path
import os
import sys
import fileinput
from shutil import copyfile

ESP8266_PACKAGE_PATH = Path("packages/esp8266/hardware/esp8266/")


def update_line_file(
        file_path, str_line_to_update, str_replacement, comment_only=False,
        comment_str=None):
    '''
    Updates a line on a file with a replacement line or comments it out

    :param file_path: The path to the file
    :type file_path: str
    :param str_to_update: The string which will be replaced
    :type str_to_update str:
    :param str_replacement: The string which replace the line of str_to_update
    :type str_replacement str:
    :param comment_only: Determines whether to replace or only comment out a
    line
    :type comment_only boolean:
    :param comment_str: Str to use for a comment if commenting
    :type comment_only str:
    :raises: :class:`FileNotFound`: File couldn't be opened

    :returns: whether the string was replaced in the file or it was commented
    out
    :rtype: boolean
    '''
    file_modified = False
    for line in fileinput.input(file_path, inplace=True):
        if line.startswith(str_line_to_update):
            if comment_only:
                line = f"{comment_str} {line}"
                file_modified = True
            elif line.rstrip() != str_replacement:
                line = f"{str_replacement}\n"
                file_modified = True
        sys.stdout.write(line)

    return file_modified


def confirm_overwrite(file_path):
    '''
    Confirms whether to overwrite changes otherwise exits program

    :param file_path: The path to the file
    :type file_path: str
    '''
    prompt = f"There is already a backup file at" \
             f" {file_path}; proceeding will" \
             f" overwrite this file. Do you wish to proceed?" \
             f" Input Y or N:" \
             f" "
    while True:
        response = input(prompt)
        response = response.lower()
        if response == 'n':
            print("No changes made... exiting")
            sys.exit()
        elif response == 'y':
            print("Backup will be overwritten")
            break
        else:
            print("Ensure your response is a Y or N")


def main():
    prompt = "This script will attempt to automatically update" \
             " your ESP8266 board files to work with Azure IoT Hub" \
             " for the repo https://github.com/Azure/azure-iot-arduino" \
             "\nPlease refer to the license agreement there." \
             "\nThis script will update all installed versions of board" \
             " libraries for ESP8266." \
             "\nDo you wish to proceed? Please answer Y or N:" \
             " "
    while True:
        response = input(prompt)
        response = response.lower()
        if response == 'n':
            print("No changes made... exiting")
            sys.exit()
        elif response == 'y':
            print("Proceeding")
            break
        else:
            print("Ensure your response is a Y or N")

    if sys.platform == "darwin":
        ARDUINO_PACKAGES_PATH = Path(Path.home() / "Library/Arduino15")
    elif sys.platform == "linux":
        # TODO: add path here!
        ARDUINO_PACKAGES_PATH = Path(Path.home() / ".arduino15/packages/")
    elif sys.platform == "win32":
        # TODO: add path here!
        ARDUINO_PACKAGES_PATH = Path(Path.home() / "AppData/Local/Arduino15")
    else:
        print(f"Error: no valid board path condition for platform:"
              f" {sys.platform}")
        sys.exit()

    print(f"Arduino board path for platform {sys.platform} is:"
          f" {ARDUINO_PACKAGES_PATH}")

    # Check for and change other versions if they exist
    versions = []
    with os.scandir(ARDUINO_PACKAGES_PATH / ESP8266_PACKAGE_PATH) as entries:
        for version in entries:
            # avoid files and hidden files
            if version.is_dir and not version.name.startswith('.'):
                versions.append(Path(ARDUINO_PACKAGES_PATH /
                                     ESP8266_PACKAGE_PATH / version))

    for path in versions:
        arduino_header_backup = Path(path / "cores/esp8266/Arduino.h.orig")
        if arduino_header_backup.exists():
            confirm_overwrite(arduino_header_backup)

        arduino_header_file = Path(path / "cores/esp8266/Arduino.h")
        if arduino_header_file.exists():
            print(f"Updating: {arduino_header_file}")
            # TODO: add logic to detect if backup file exists then skip
            copyfile(arduino_header_file,
                     Path(path / "cores/esp8266/Arduino.h.orig"))
            print(
                f"Backup created:"
                f" {Path(path / 'cores/esp8266/Arduino.h.orig')}")
            get_update = update_line_file(
                arduino_header_file, "#define round(x)", str_replacement=None,
                comment_only=True, comment_str="//")
            print(f"Updated: {get_update} for {arduino_header_file}")

        platform_txt_backup = Path(path / "platform.txt.orig")
        if platform_txt_backup.exists():
            confirm_overwrite(platform_txt_backup)

        platform_txt_file = Path(path / "platform.txt")
        if platform_txt_file.exists():
            print(f"Updating: {platform_txt_file}")
            copyfile(platform_txt_file, Path(path / "platform.txt.orig"))
            print(f"Backup created: {Path(path / 'platform.txt.orig')}")
            get_update = update_line_file(
                    platform_txt_file, "build.extra_flags=",
                    str_replacement="build.extra_flags=-DESP8266"
                    " -DDONT_USE_UPLOADTOBLOB -DUSE_BALTIMORE_CERT")
            print(f"Updated: {get_update} for {platform_txt_file}")


main()
