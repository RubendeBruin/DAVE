import re


def increment_string_end(s):
    match = re.search(r"\d+$", s)
    if match:
        end_num = match.group()
        start_index = s.rfind(end_num)
        incremented_num = str(int(end_num) + 1)
        return s[:start_index] + incremented_num
    else:
        return s + "2"

def code_to_blocks(code : str, code_bewteen_empty_lines_is_a_block = True):
    """Splits the code into blocks of complete python code.

    Code is a block if:
    - the syntax demands it (indentation, brackets, braces, etc.)
    - the code is between two empty lines (if code_bewteen_empty_lines_is_a_block is True)


    """


    lines = code.split('\n')

    blocks = []
    brackets = 0
    braces = 0
    within_tripplequotes = False
    previous_line_ends_with_backslash = False

    previous_line_empty = False

    for line in lines:

        line_is_empty = line.strip() == ''


        if not line_is_empty:

            if (line.startswith(' ') or
                    line.startswith('\t') or
                    brackets!=0 or
                    braces!=0 or
                    previous_line_ends_with_backslash or
                    within_tripplequotes or
                    (not previous_line_empty and code_bewteen_empty_lines_is_a_block)):
                if blocks:
                    blocks[-1] += '\n' + line
                else:
                    blocks.append(line)
            else:
                blocks.append(line)

            # count the number of [ brackets in the line to see if we need to continue the block

            brackets += line.count('[')
            braces += line.count('(')

            brackets -= line.count(']')
            braces -= line.count(')')

            for i in range(line.count('"""')):
                within_tripplequotes = not within_tripplequotes

            previous_line_ends_with_backslash = line.strip().endswith('\\')

        previous_line_empty = line_is_empty

    return blocks





if __name__ == "__main__":
    print(increment_string_end("hello123"))  # Output: hello124
    print(increment_string_end("hello"))  # Output: hello2
