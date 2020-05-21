import sys

if sys.platform == "darwin":
    # TODO: add path here!
    ARDUINO_BOARD_PATH = ""
    print("it's a mac")
elif sys.platform == "linux":
    # TODO: add path here!
    ARDUINO_BOARD_PATH = ""
    print("it's linux i broke it")
elif sys.platform == "win32":
    # TODO: add path here!
    ARDUINO_BOARD_PATH = ""
    print("it's Windows")

# TODO: this is a work in progress and needs to be implemented!
def update_line_file(file_path, str_line_to_update, str_replacement, comment_only):
    '''
    Updates a line on a file with a replacement line or comments it out

    :param file_path: The path to the file 
    :type file_path: str
    :param str_to_update: The string which will be replaced
    :type str_to_update str:
    :param str_replacement: The string which replace the line of str_to_update
    :type str_replacement str:
    :param comment_only: Determines whether to replace or only comment out a line
    :type comment_only boolean:
    :raises: :class:`FileNotFound`: File couldn't be opened

    :returns: whether the string was replaced in the file or it was commented out
    :rtype: boolean
    '''
    # ! Important; this updates an entire line! If the substring matches
    #  the line should be obliterated and replaced with str_replacement
    file_modified = False
    return file_modified

def main():
    # check if board path is set
    try: 
        print(f"Your Arduino board path is: {ARDUINO_BOARD_PATH}")
    except NameError:
        print(f"Error: no valid board path condition for platform: {sys.platform}")
main()