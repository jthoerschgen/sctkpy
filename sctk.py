# -*- coding: utf-8 -*-

import argparse
import re

import sctkpy.core
import sctkpy.db_funcs


def validate_term(term: str):
    """Given a term, validate that it is in the correct format

    Args:
        term (str): Term string to test

    Raises:
        AssertionError: Term does not match correct regular expression pattern
    """
    try:
        assert re.match(
            r"^(FS|SP)\d{4}$", term
        ), "Term must be in format 'SPXXXX' or 'FSXXXX'"
    except AssertionError as exc:
        print(f"Error: {exc}")


def main():
    """Main function that handles argparse stuff"""
    sctkpy.db_funcs.load_roster_into_db()
    sctkpy.db_funcs.load_grades_into_db()

    parser = argparse.ArgumentParser(
        prog="sctkpy",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=r"""
 _____  _   _  ____                                                 #@@@%#*=-
|_   _|| |_| || ===|                                              +@@@@@@@@@@@@@@%*+=:
  |_|  |_| |_||____|                                            -@@@@%@@@@@@@@@@@@@@@@@+
  ____  ____  _   _  ____  _      ____  _____   ____  _   _  _ @@@@@@@-    =#@@@@@@@@@*
 (_ (_`/ (__`| |_| |/ () \| |__  / () \ | () ) (_ (_`| |_| || || ()_)%#+-      :@@@@%:
.__)__)\____)|_| |_|\____/|____|/__/\__\|_|\_\.__)__)|_| |_||_||_|@@@@@@@@@@@%%@@@@-:%@-
 ____  _   _   ____  _____  _  __  __   ____   __  _ , ____@@@@@@@@@@@@@@@@@@@@@@*  +@@:
/ (__`| |_| | / () \ | () )| ||  \/  | / () \ |  \| | (_ (_`@@@@@@@@@@@@@@@@@@@@:   -@@-
\____)|_| |_|/__/\__\|_|\_\|_||_|\/|_|/__/\__\|_|\__|.__)__)@@@@@@@@@@@@@@@@@@=   :%@@*
 _____  ____  ____  _     __  __  _  _____           :%@@@@@@@@@@@@@@@@@@@@@#    +@@%:
|_   _|/ () \/ () \| |__ |  |/  /| ||_   _|          =@@-    :=*%@@@@@@@@@%:   :%@@=
  |_|  \____/\____/|____||__|\__\|_|  |_|            =@@-           :+%@@+    +@@%
                                                      %@@:                  -@@@=
    Copyright © 2024 By: Jimmy Hoerschgen              +@@@@@%*-           #@@#
                                                          -+#@@@@@@%*=:  =@@@-
    A tool for aiding in the duties of the                      :=#%@@@@@@@*
    scholarship chairman.                                              -*#:
    """,
        epilog="and don't forget to do your homework",
    )

    parser.add_argument(
        "--report",
        action="store",
        type=str,
        help="generate grade report for a term, (eg. SPXXXX, FSXXXX)",
        metavar="TERM",
        nargs="?",
    )
    parser.add_argument(
        "--checklist",
        action="store",
        type=str,
        help="generate study-checklist for a term, (eg. SPXXXX, FSXXXX)",
        metavar="TERM",
        nargs="?",
    )
    parser.add_argument(
        "--files",
        action="store",
        type=str,
        help="generate files turn-in list for a term, (eg. SPXXXX, FSXXXX)",
        metavar="TERM",
        nargs="?",
    )
    args = parser.parse_args()

    if args.report is not None:
        validate_term(args.report)
        sctkpy.core.generate_grade_report(term=args.report)
    if args.checklist is not None:
        validate_term(args.checklist)
        sctkpy.core.generate_study_check_sheet(term=args.checklist)
    if args.files is not None:
        validate_term(args.files)
        sctkpy.core.generate_files_responsibility_report(term=args.files)

    return


if __name__ == "__main__":
    main()
