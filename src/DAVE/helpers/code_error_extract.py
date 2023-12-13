import sys
import traceback


def get_code_error(code):
    """Call this when an error was raised when executing code.
    Use the trackback functionality to extract a clear message"""

    # get the type of the last exception
    # if it is a SyntaxError, we can extract the line number


    # get traceback to code
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback_details = traceback.extract_tb(exc_traceback)

    if exc_type == SyntaxError:
        # code_error = f"Syntax error on line {exc_value.lineno}: {exc_value.text}"
        line_number = exc_value.lineno
    else:
        filename, line_number, func_name, text = traceback_details[1]  # get the last frame

    code_error = f"An error occurred on line {line_number}: "

    lines = code.split("\n")
    start = max(0, line_number - 5)
    end = min(len(lines), line_number + 5)
    for i in range(start, end):
        code_error += f"\n{i + 1}:      {lines[i]}"

    return code_error

