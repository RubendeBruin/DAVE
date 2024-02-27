# Runner is a class that will
# The class is created with a filename (.md) as argument
# it will extract the directory where the .md file is located as will set that as the working directory
# the file is then read and the code is extracted
# the code is identified by the following patterns:
# ```load
# code
# ```
# or
# ```actions
# code
# ```
# or
# ```assertions
# code
# ```
import os
from math import log10
from pathlib import Path

from numpy import allclose, log

import DAVE.settings as ds


HEADER = """
Test results:

| Value | Actual | Expected | Tol  | Description                                                  |
| ----- | ------ | -------- | ---- | ------------------------------------------------------------ |
"""

# Assertions are of the form:
# value = ...
# expect = {value}
# {description}

# the assertion is then executed based on the number of decimal values in expect

# Finally the result is saved to a .md file in the same folder.

class Assertion():

        def __init__(self):
            self.value = None
            self.evaluated = None
            self.expect = None
            self.tolerance = 1e-3
            self.description = ""

            self.result = None  # not run

        def is_empty(self):
            return self.value is None and self.expect is None

        def execute(self, s):
            #
            if self.value is None:
                raise ValueError("Value not set")

            import DAVE

            locals = DAVE.__dict__
            locals["s"] = s

            locals.update(ds.DAVE_ADDITIONAL_RUNTIME_MODULES)

            try:
                self.evaluated = eval(self.value, {}, locals)

            except Exception as e:
                self.result = False
                self.description += f"\n\nError in value: {e}"
                return

            # no expect, just check if value evaluates to true
            if self.expect is None:
                if self.evaluated:
                    self.result = True
                    return

            expect = eval(self.expect, {}, locals)

            # if the values are plain equal then the result is ok
            if self.evaluated == expect:
                self.result = True
                return


            # but we can also check if the values are close
            if allclose(self.evaluated, expect, atol=self.tolerance):
                self.result = True
                return

            self.result = False





        def save(self):
            pass

def parse_assertions(code):
    assertions = [Assertion()]

    for line in code.split('\n'):
        if line.strip() == "":
            assertions.append(Assertion())  # empty line, start a new assertion
            continue

        token = line.split('=')[0].strip()

        if token.lower() == 'value':
            assertions[-1].value = line.split('=')[1].strip()
        elif token.lower() == 'expect':
            assertions[-1].expect = line.split('=')[1].strip()
        elif token.lower() == 'tol':
            assertions[-1].tolerance = float(line.split('=')[1].strip())
        else:
            if assertions[-1].description == "":
                assertions[-1].description = line.strip()
            else:
                assertions[-1].description = assertions[-1].description  + "<br>"+line.strip()

    return [a for a in assertions if not a.is_empty()]

class DaveTestRunner():

    def __init__(self, filename : Path):

        if not isinstance(filename, Path):
            filename = Path(filename)

        self.filename = filename
        self.working_directory = filename.parent
        self.code = self.read_file()
        self.load_code = self.extract_code('load')
        self.actions_code = self.extract_code('actions')
        self.assertions_code = self.extract_code('assert')

        self.passed = None
        self.result_filename = None

        self.level1 = filename.parent.parent.name
        self.level2 = filename.parent.name

        self.run_code()



    def read_file(self):
        with open(self.filename, 'r') as file:
            return file.read()

    def extract_code(self, code_type):
        start = f'```{code_type}\n'
        end = '```'

        start_index = self.code.find(start)
        if start_index == -1:
            return ""

        end_of_start = start_index + len(start)

        end_index = self.code.find(end, end_of_start)
        return self.code[end_of_start:end_index]

    def run_code(self):

        from DAVE import Scene

        s = Scene()

        s.load(self.working_directory / self.load_code.strip())

        s.run_code(self.actions_code)

        # parse the assertions
        # value = ...
        # expect = {value}
        # [tol = ...]
        # {description}
        # the assertion is then executed based on the number of decimal values in expect
        # Finally the result is saved to a .md file in the same folder.

        assertions = parse_assertions(self.assertions_code)

        for assertion in assertions:
            assertion.execute(s)

        # did we pass?
        self.passed = all([a.result for a in assertions])

        # make a copy of the input file
        # using the same name + _result
        # and in the same folder

        self.result_filename = self.filename.with_name(self.filename.stem + "_result.md")
        with open(self.filename.parent / self.result_filename, 'w') as file:

            file.write(f"# {self.level1} / {self.level2} / {self.filename.stem}\n\n")

            if self.passed:
                file.write("PASSED \n")
            else:
                file.write("FAILED \n")

            file.write(HEADER)

            for assertion in assertions:

                if not self.passed and assertion.result:  # only list failed assertions
                    continue

                file.write(f"| {assertion.value} | ")

                v = assertion.evaluated
                decimals = -int(log10(assertion.tolerance))
                if isinstance(v, (int, float)):
                    # round to tolerance
                    v = round(v, decimals)
                    file.write(f"{v} | ")
                elif isinstance(v, (list, tuple)):
                    file.write("<br>".join([str(round(x, decimals)) for x in v]) + " | ")
                else:
                    file.write(f"{assertion.evaluated} | ")

                # format the expected value
                if assertion.expect is not None:
                    v = eval(assertion.expect)
                    if isinstance(v, (list, tuple)):
                        file.write("<br>".join(str(s) for s in v) + " | ")
                    else:
                        file.write(f"{assertion.expect} | ")
                    file.write(f"{assertion.tolerance} | ")
                else:
                    file.write(f" True | | ")
                file.write(f"{assertion.description} |\n")

            file.write('\n\n')

            file.write(self.code)




def run_tests(root):

    filenames = []

    for filename in root.glob("**/**/*.md"):
        if f"\_build\\" in str(filename):
            continue

        if filename.stem.endswith("_result"):
            continue

        if filename == root / "welcome.md":
            continue

        filenames.append(filename)

    for file in filenames:
        print(file)
    tests = []

    # ROOT / level1 / level2 / filename

    errors = []
    for filename in filenames:
        try:
            print('Running', filename)
            test = DaveTestRunner(filename)
            tests.append(test)
            if test.passed:
                print(f"{filename} passed")
            else:
                print(f"{filename} failed")
        except Exception as e:
            errors.append(f"Failed to run {filename} with error: {e}")
            print(f"Failed to run {filename} with error: {e}")

    YML_header = """format: jb-book\nroot: welcome\nparts:"""

    YML_passed = """-  caption: Passed\n   chapters:"""

    YML_failed = """-  caption: Failed\n   chapters:"""

    toc_file = root / "_toc.yml"

    passed = [t for t in tests if t.passed]
    failed = [t for t in tests if not t.passed]

    with open(toc_file, 'w') as file:
        file.write(YML_header + "\n")
        if passed:
            file.write(YML_passed + "\n")
            for test in passed:
                file.write(f"   - file: {test.level1}/{test.level2}/{test.result_filename.stem}\n")

        if failed:
            file.write(YML_failed + "\n")
            for test in failed:
                file.write(f"   - file: {test.level1}/{test.level2}/{test.result_filename.stem}\n")

    # write a summary file (welcome.md)

    with open(root / "welcome.md", 'w') as file:
        file.write("# Welcome to DAVE test suite\n\n")
        file.write("This is the result of the tests\n\n")

        if errors:
            file.write("## Errors\n\n")
            for error in errors:
                file.write(f"- {error}\n\n")

        file.write("## Passed tests\n\n")
        for test in passed:
            file.write(f"- {test.level1} / {test.level2} / {test.result_filename.stem}\n\n")

        file.write("## Failed tests\n\n")
        for test in failed:
            file.write(f"- {test.level1} / {test.level2} / {test.result_filename.stem}\n\n")

    print("Done!")

