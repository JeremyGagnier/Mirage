import inspect
import traceback
import sys


class UnexpectedResultException(Exception):
    pass


def verify_result(a, b):
    if (a != b):
        a_str = str(a)
        if type(a) == type([]):
            a_str = f"[{', '.join(list(map(lambda x: str(x), a)))}]"

        b_str = str(b)
        if type(b) == type([]):
            b_str = f"[{', '.join(list(map(lambda x: str(x), b)))}]"

        raise UnexpectedResultException(f"Expected \"{a_str}\" to be equal to \"{b_str}\"")


def run_tests(*test_functions):
    print(f"Running {len(test_functions)} tests")
    failures = 0
    message_on_failure = ""
    for test_function in test_functions:
        if not inspect.isfunction(test_function) or test_function.__name__ == '<lambda>':
            raise Exception(f"run_tests only takes named function arguments, got {test_function}")

        try:
            test_function()
            print(".", end="")
        except Exception as e:
            failures += 1
            trace_string = "".join(traceback.format_exception(None, e, e.__traceback__))
            message_on_failure += f"{failures} Test {test_function.__name__} failed with exception:\n{trace_string}"
            print("E", end="")

    print()
    if failures > 0:
        print(message_on_failure)
        print(f"{failures} failures")
        print("FAILURE")

    else:
        print("SUCCESS")
