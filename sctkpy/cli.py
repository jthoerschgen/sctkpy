"""The command-line interface for generating academic reports."""

import argparse
import random
import re

from sctkpy.reports.files_report import FilesReport
from sctkpy.reports.member_report import MemberReport
from sctkpy.reports.study_check_report import StudyCheckReport
from sctkpy.reports.study_hour_report import StudyHourReport


def validate_term(term: str) -> None:
    """Given a term, validate that it is in the correct format

    Args:
        term (str): Term string to test

    Raises:
        ValueError: Term does not match correct regular expression pattern

    Returns:
        None: None
    """
    if not re.match(r"^(FS|SP)\d{4}$", term):
        raise ValueError("Term must be in format 'SPXXXX' or 'FSXXXX'")


def main() -> None:
    """Main function that handles argparse stuff"""

    parser = argparse.ArgumentParser(
        prog="sctkpy",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=r"""
 _____  _   _  ____                                                 #@@@%#*=-
|_   _|| |_| || ===|                                              +@@@@@@@@@@@@@@%*+=:
  |_|  |_| |_||____|                                            -@@@@%@@@@@@@@@@@@@@@@@+
  ____  ____  _   _  ____  _      ____  _____   ____  _   _  _ @@@@@@@- SC =#@@@@@@@@@*
 (_ (_`/ (__`| |_| |/ () \| |__  / () \ | () ) (_ (_`| |_| || || ()_)%#+- TK   :@@@@%:
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
        epilog=random.choice(
            [
                '"...and don\'t forget to do your homework."',
                '"Those found not studying will be beat severely."',
                '"Use at your own risk."',
                '"May contain dairy."',
                '"I love my rabbit, Peter."',
            ]
        ),
    )

    report_type_options: list[str] = [
        "study-hours",
        "study-checks",
        "files-list",
        "member-report",
    ]
    parser.add_argument(
        "--report-type",
        action="store",
        type=str,
        choices=report_type_options,
        help=f"Type of Grade Report. Options: {','.join(report_type_options)}",
        metavar="TYPE",
    )

    parser.add_argument(
        "--roster",
        action="store",
        type=str,
        help="File path to 'greeklife_roster_report.csv'",
        metavar="PATH",
    )

    parser.add_argument(
        "--report-dir",
        action="store",
        type=str,
        help="File path to directory of 'XXXXXX_ind_grade_report.csv' files.",
        metavar="PATH",
    )

    parser.add_argument(
        "--save-dir",
        action="store",
        type=str,
        help="File path to directory of save location.",
        metavar="PATH",
    )

    parser.add_argument(
        "--term",
        action="store",
        type=str,
        help="Generate grade report for a term, (eg. SPXXXX, FSXXXX)",
        metavar="TERM",
    )

    args = parser.parse_args()

    if not args.roster:
        parser.error("--roster is required for this operation.")
    if not args.report_dir:
        parser.error("--report-dir is required for this operation.")
    if (
        args.report_type in ["study-hours", "study-checks", "files-list"]
        and not args.term
    ):
        parser.error("--term is required for this report type.")

    if args.report_type == "study-hours":
        validate_term(args.term)
        study_hour_report = StudyHourReport(
            roster_report_path=args.roster, save_dir=args.save_dir
        )
        study_hour_report.add_grade_report_dir(
            grade_report_dir_path=args.report_dir
        )
        study_hour_report(selected_term=args.term, open_on_finish=True)

    if args.report_type == "study-checks":
        validate_term(args.term)
        study_check_report = StudyCheckReport(
            roster_report_path=args.roster, save_dir=args.save_dir
        )
        study_check_report.add_grade_report_dir(
            grade_report_dir_path=args.report_dir
        )
        study_check_report(selected_term=args.term, open_on_finish=True)

    if args.report_type == "files-list":
        validate_term(args.term)
        files_report = FilesReport(
            roster_report_path=args.roster, save_dir=args.save_dir
        )
        files_report.add_grade_report_dir(
            grade_report_dir_path=args.report_dir
        )
        files_report(selected_term=args.term, open_on_finish=True)

    if args.report_type == "member-report":
        member_report = MemberReport(
            roster_report_path=args.roster, save_dir=args.save_dir
        )
        member_report.add_grade_report_dir(
            grade_report_dir_path=args.report_dir
        )
        member_report()


if __name__ == "__main__":
    main()
