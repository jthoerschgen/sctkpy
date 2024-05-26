# -*- coding: utf-8 -*-

import csv
import io

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from .config import (
    default_roster_csv_path,
    term_gpa_strike,
)  # cumulative_gpa_strike,
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


def plot_member_gpa(
    member: Member, show_plot: bool = False
) -> Image.Image | None:
    """Generate a plot of a given member's term and cumulative GPA and show
    academic strikes

    Args:
        member (Member): Member to plot grade data from
        show_plot (bool, optional): Show plot when done. Defaults to False.

    Returns:
        Image.Image | None: Return plot as PNG image
    """
    terms_list, term_gpa_list, cumulative_gpa_list = (
        member.generate_academic_report()
    )
    if len(terms_list) == 0:
        return None

    terms_array = np.arange(len(terms_list))

    term_gpas = np.array(term_gpa_list).astype(np.double)
    term_gpas_mask = np.isfinite(term_gpas)

    cumulative_gpas = np.array(cumulative_gpa_list).astype(np.double)
    cumulative_gpas_mask = np.isfinite(cumulative_gpas)

    fig, ax = plt.subplots()

    ax.set_title(f"Grades for {member.name}")
    ax.set_xlabel("Term")
    ax.set_ylabel("GPA")

    ax.grid()

    # resize y-axis limit
    ax.set_ylim([0.00, 4.00])

    # Set x-axis to term names
    ax.set_xticks(terms_array)
    ax.set_xticklabels(
        [terms_list[i] for i in terms_array[cumulative_gpas_mask]], rotation=45
    )

    # plot term gpas
    ax.plot(
        terms_array[term_gpas_mask],
        term_gpas[term_gpas_mask],
        label="Term GPA",
        color="blue",
    )

    # plot cumulative gpas
    ax.plot(
        terms_array[cumulative_gpas_mask],
        cumulative_gpas[cumulative_gpas_mask],
        label="Cumulative GPA",
        color="orange",
    )

    # labeling data
    for term, (term_gpa, cumulative_gpa) in zip(
        terms_array, zip(term_gpas, cumulative_gpas)
    ):
        if not np.isnan(term_gpa):
            y_offset = -1 if term_gpa == min(term_gpa, cumulative_gpa) else 1
            ax.annotate(
                f"{term_gpa:.3f}",
                xy=(term, term_gpa),
                xytext=(term, term_gpa + 0.15 * y_offset),
                arrowprops={
                    "width": 5,
                    "headwidth": 5,
                    "headlength": 5,
                    "shrink": 5,
                    "color": (
                        "red"
                        if term_gpa_strike.test_tier(term_gpa)
                        else "blue"
                    ),
                },
                label="Term GPA",
            )

        if not np.isnan(cumulative_gpa):
            y_offset = (
                -1 if cumulative_gpa == min(term_gpa, cumulative_gpa) else 1
            )
            ax.annotate(
                f"{cumulative_gpa:.3f}",
                xy=(term, cumulative_gpa),
                xytext=(term, cumulative_gpa + 0.15 * y_offset),
                arrowprops={
                    "width": 5,
                    "headwidth": 5,
                    "headlength": 5,
                    "shrink": 5,
                    "color": (
                        # "red"
                        # if cumulative_gpa_strike.test_tier(cumulative_gpa)
                        # else "orange"
                        "orange"
                    ),
                },
                label="Cumulative GPA",
            )

    # legend information
    ax.scatter([], [], color="red", label="Strike", marker="^", s=25)
    # ax.legend()

    buff = io.BytesIO()
    ax.get_figure().savefig(buff, format="PNG")
    buff.seek(0)

    if show_plot:
        plt.show()

    plt.close()

    return Image.open(buff)
