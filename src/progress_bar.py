import os
import re
import sys

if sys.platform == "win32":
    import ctypes
else:
    import termios

CLEAR = "\033[0J"


def enable_ansi_escape_characters():
    if sys.platform == "win32":
        stdin_mode = ctypes.c_ulong()
        stdout_mode = ctypes.c_ulong()
        kernel32 = ctypes.windll.kernel32
        kernel32.GetConsoleMode(kernel32.GetStdHandle(-10), ctypes.byref(stdin_mode))
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 0)
        kernel32.GetConsoleMode(kernel32.GetStdHandle(-11), ctypes.byref(stdout_mode))
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        return stdin_mode, stdout_mode
    else:
        stdin_mode = termios.tcgetattr(sys.stdin)
        _ = termios.tcgetattr(sys.stdin)
        _[3] = _[3] & ~(termios.ECHO | termios.ICANON)
        termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, _)

        return stdin_mode, None


def disable_ansi_escape_characters(stdin_mode, stdout_mode):
    if sys.platform == "win32":
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), stdin_mode)
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), stdout_mode)
    else:
        termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, stdin_mode)


def get_cursor_position():
    """
    returns terminal cursor position using ansi characters

    modified from the following answer:

    https://stackoverflow.com/questions/35526014
    """
    stdin_mode, stdout_mode = enable_ansi_escape_characters()

    try:
        result = ""
        print("\033[6n", end="", flush=True)
        while not (result := result + sys.stdin.read(1)).endswith("R"):
            pass
        match = re.match(r".*\[(?P<y>\d+);(?P<x>\d+)R", result)
    finally:
        disable_ansi_escape_characters(stdin_mode, stdout_mode)
    if match:
        return (int(match.group("x")), int(match.group("y")))
    return (-1, -1)


def progressbar(it, count, prefix="", size=60, with_item=True):  # Python3.6+
    """
    displays a progress bar for an iterator

    modified from the following answer:
    1. to work with generators without listing them
    2. to provide the value of the last item as a postfix.
    3. to clear the screen using ansi escape characters to fix overflowing output

    https://stackoverflow.com/a/34482761
    """

    def show(current, x, y, item=""):
        print(f"\033[{y};{x}f", end="", flush=True)
        print(CLEAR, end="", flush=True)

        filled = int(size * current / count)
        line = f"{prefix}[{'#' * filled}{('.' * (size - filled))}] {current}/{count}"  # noqa: E501
        if with_item:
            line += f" [{item}]"
        print(line, end="", flush=True)

        return len(line)

    x, y = get_cursor_position()
    max_x, max_y = os.get_terminal_size()
    show(0, x, y)
    if y == max_y:
        offset = 0
        for i, item in enumerate(it):
            line_length = show(i + 1, x, y - offset, str(item))
            offset += int(line_length / (max_x * (offset + 1)))

            yield item
    else:
        for i, item in enumerate(it):
            show(i + 1, x, y, str(item))

            yield item

    print("\n", flush=True)
