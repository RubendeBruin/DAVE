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


if __name__ == "__main__":
    print(increment_string_end("hello123"))  # Output: hello124
    print(increment_string_end("hello"))  # Output: hello2
