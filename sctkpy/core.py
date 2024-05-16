# -*- coding: utf-8 -*-

import csv

from .config import default_roster_csv_path
from .member import Member


def parse_roster_report(
    csv_file_path: str | None = None, rows_to_header: int = 3
) -> tuple[str, list[tuple[str, str, str]]]:
    """Parses the "greeklife_roster_report.csv" either from a given path or
    via the root of the project directory. Saves the results and inserts/
    updates member information in SQLite.

    Args:
        csv_file_path (str | None, optional):
            Optional path to csv file. Defaults to None.
        rows_to_header (int, optional):
            Rows to skip to get the the header. Defaults to 3.

    Returns:
        Roster term,
        List of strings of First Name, Last Name, and In/Out House status
    """

    if csv_file_path is None:
        csv_file_path = default_roster_csv_path

    with open(csv_file_path, "r", encoding="utf-8") as csv_file:
        for _ in range(rows_to_header):  # Skip first rows to get to head
            next(csv_file)
        dr = csv.DictReader(csv_file)
        raw_member_info: list[tuple[str, str, str, str]] = sorted(
            list(
                {
                    (
                        row["First Name"],
                        row["Last Name"],
                        row["in/out House"],
                        row["Term"],
                    )
                    for row in dr
                }
            ),
            key=lambda tup: (1 if tup[2] == "IN" else 0, tup[1]),
        )
        member_info: list[tuple[str, str, str]] = [
            row[:3] for row in raw_member_info
        ]
        assert (
            len({row[3] for row in raw_member_info}) == 1
        ), "More than one unique term in roster"
        term = {row[3] for row in raw_member_info}.pop()

    return term, member_info


def get_member_info() -> list[Member]:
    """Gets list of dudes from grade report and spits them out

    Returns:
        list[Member]: List of Member objects
    """
    _, member_info = parse_roster_report()
    members = [
        Member(
            name=" ".join(member[:2]),
            out_of_house=True if member[2] == "OUT" else False,
        )
        for member in member_info
    ]

    return sorted(
        members,
        key=lambda dude: (
            not dude.out_of_house,
            (
                int(dude.pledge_class[2:])
                if dude.pledge_class is not None
                else float("inf")  # if no pledge class, goes last
            ),
            (
                (0 if dude.pledge_class[:2] == "SP" else 1)
                if dude.pledge_class is not None
                else float("inf")  # if no pledge class, goes last
            ),
            dude.name.split()[1],
        ),  # Sort by year, semester (SP/FS), then last name
    )
