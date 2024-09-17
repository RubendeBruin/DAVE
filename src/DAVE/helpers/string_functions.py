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

def code_to_blocks(code : str):
    """Splits the code into blocks of complete python code.

    """


    lines = code.split('\n')


    blocks = []
    brackets = 0
    braces = 0
    within_tripplequotes = False
    previous_line_ends_with_backslash = False


    for line in lines:
        if line.strip():  # skip empty lines

            if (line.startswith(' ') or
                    line.startswith('\t') or
                    brackets!=0 or
                    braces!=0 or
                    previous_line_ends_with_backslash or
                    within_tripplequotes):
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

    return blocks





if __name__ == "__main__":
    print(increment_string_end("hello123"))  # Output: hello124
    print(increment_string_end("hello"))  # Output: hello2
