#! /usr/bin/python3
# -*- coding: utf-8 -*-

from sys import argv
from os.path import basename
from typing import List
from polls.test.resource import MOCK_DEPARTMENTS, MOCK_EMPLOYEES
from polls.test.testing_utils import create_departments, create_employees


def main(option_list: List[str]):
    """
    Sends HTTP requests to create mock data according to the given command line options.
    :param option_list: Command line options
    """

    if "verbose" in option_list:
        verbose = True
        option_list.remove("verbose")
    else:
        verbose = False

    for option in option_list:
        if option == "mock-departments":
            create_departments(MOCK_DEPARTMENTS, verbose)
        elif option == "mock-employees":
            create_employees(MOCK_EMPLOYEES, verbose)
        elif option == "help":
            show_usage()
            # exit(0)
        else:
            print(f"Unknown mock option {option}")
            show_usage()
            exit(1)


def show_usage():
    """
    Shows the usage page.
    """

    usage_screen = "\nUsage:\n" \
                   f"    {basename(argv[0])} <mock_1> [<mock_2> ...]\n" \
                   "\nOptions:\n" \
                   "    mock-departments     Send HTTP requests to create some mock departments in the backend.\n" \
                   "    mock-employees       Send HTTP requests to create some mock employees in the backend.\n" \
                   "    help                 Show this help page.\n" \
                   "" \
                   "    verbose              Enables detailed request logging for the remaining options.\n"
    print(usage_screen)


if __name__ == "__main__":
    if len(argv) < 2:
        show_usage()
        exit(1)
    main(argv[1:])
