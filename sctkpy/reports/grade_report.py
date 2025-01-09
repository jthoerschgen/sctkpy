"""Base Class for Generating Grade Reports."""

import csv
import os

from sctkpy.member.course import Course, Grade
from sctkpy.member.member import Member
from sctkpy.member.term import Term


class GradeReport:
    """Object used for parsing and collecting grade report information.

    Takes a roster report and collects grade data from individual grade
    reports that is for members in the roster report.

    Attributes:
        self.members (dict[str, Member]): A dictionary of member objects where
            the key is the name of the member and the value is a blank Member
            object by default.
    """

    def __init__(self, roster_report_path: str | None = None):
        self.members: dict[str, Member] = (
            self.parse_roster_report(roster_report_path)
            if roster_report_path is not None
            else dict()
        )

    def parse_roster_report(
        self, roster_report_path: str, rows_to_header: int = 3
    ) -> dict[str, Member]:
        """Parse the Greek-life Roster Report into a list of Members.

        Args:
            roster_report_path (str): The file path of the roster report csv
                file.
            rows_to_header (int, optional): The number of rows that are before
                the header of the data. Defaults to 3.

        Raises:
            FileExistsError: No file exists for the roster report path.
            ValueError: The roster report path is not for a csv file.
            ValueError: The roster report csv file has unexpected headers.
            ValueError: The roster report 'in/out House' column is not
                exclusively the values 'IN' or 'OUT'.

        Returns:
            dict[str, Member]: Dictionary of Member objects where the key is'
                the name of the Member.
        """
        if not os.path.exists(roster_report_path):
            raise FileExistsError(f"{roster_report_path} doe not exists.")
        if not roster_report_path.endswith(".csv"):
            raise ValueError(f"{roster_report_path} is not a CSV file.")

        members: dict[str, Member] = dict()
        with open(roster_report_path, mode="r", encoding="utf-8") as csv_file:
            for _ in range(rows_to_header):  # skip first rows
                next(csv_file)
            reader = csv.DictReader(csv_file)

            expected_report_header = [
                "Last Name",
                "First Name",
                "Chapter Name",
                "in/out House",
                "Email",
                "Term",
            ]
            if reader.fieldnames != expected_report_header:
                raise ValueError(
                    f"Error When Reading CSV file: {roster_report_path}, "
                    + "Unexpected Header for CSV file, "
                    + f"Expected: {expected_report_header} "
                    + f"on row {rows_to_header + 1}"
                )

            for row in reader:
                if row["in/out House"] not in ["IN", "OUT"]:
                    raise ValueError(
                        f"Error When Reading CSV file: {roster_report_path}, "
                        + "in/out House value must be either 'IN' or 'OUT'"
                    )

                name: str = f"{row["First Name"]} {row["Last Name"]}"
                out_of_house: bool = (
                    True if row["in/out House"] == "OUT" else False
                )

                members[name] = Member(name, out_of_house)
        return members

    def add_grade_report(
        self,
        grade_report_path: str,
        rows_to_header: int = 2,
    ) -> None:
        """Parse an Individual Grade Report and use it to update Members.

        The information from the Individual Grade Report is parsed, validated,
        and is added or updates the grade information for each member which is
        included in the report.

        The function returns nothing, the members attribute is updated in-
        place.

        Args:
            grade_report_path (str): The path of the individual grade report
                csv file.
            rows_to_header (int, optional): The number of rows that are before
                the header of the data. Defaults to 2.

        Raises:
            FileExistsError: No file exists for the grade report path.
            ValueError: The grade report path is not for a csv file.
            ValueError: The grade report csv file has unexpected headers.
            ValueError: The grade report 'New Member' column is not
                exclusively the values 'Y' or 'N'.
            ValueError: Columns values for all rows associated with a member
                that are supposed to all be the same value are not.

        Returns:
            None: None
        """
        if not os.path.exists(grade_report_path):
            raise FileExistsError(f"{grade_report_path} doe not exists.")
        if not grade_report_path.endswith(".csv"):
            raise ValueError(f"{grade_report_path} is not a CSV file.")

        member_dict: dict[str, list[dict[str, str]]] = dict()
        for member_name in self.members:
            member_dict[member_name] = list()

        with open(grade_report_path, mode="r", encoding="utf-8") as csv_file:
            for _ in range(rows_to_header):  # skip first rows
                next(csv_file)
            reader = csv.DictReader(csv_file)

            expected_report_header = [
                "Name",
                "Term",
                "Chapter",
                "New Member",
                "Enroll Hrs",
                "Priv GPA",
                "Priv Cum GPA",
                "Term GPA",
                "Term Cum GPA",
                "Class",
                "Catalog No",
                "Hrs",
                "Grade",
                "Grade Type",
            ]
            if reader.fieldnames != expected_report_header:
                raise ValueError(
                    f"Error When Reading CSV file: {grade_report_path}, "
                    + "Unexpected Header for CSV file, "
                    + f"Expected: {expected_report_header} "
                    + f"on row {rows_to_header + 1}"
                )

            for row in reader:
                if row["New Member"] not in ["Y", "N"]:
                    raise ValueError(
                        f"Error When Reading CSV file: {grade_report_path}, "
                        + "Values for column 'New Member' must be either: "
                        + "'Y' or 'N'."
                    )

                member: list[dict[str, str]] | None = member_dict.get(
                    row["Name"]
                )
                if member is None:
                    continue

                member_dict[row["Name"]].append(row)

        for name, rows in member_dict.items():
            if len(rows) == 0:
                continue

            # Data validation
            columns_with_same_row_data: list[str] = [
                "Name",
                "Term",
                "Chapter",
                "New Member",
                "Enroll Hrs",
                "Priv GPA",
                "Priv Cum GPA",
                "Term GPA",
                "Term Cum GPA",
            ]
            for column in columns_with_same_row_data:
                if len({row[column] for row in rows}) != 1:
                    raise ValueError(
                        f"Cannot have different '{column}' values for member."
                    )

            # Create Term
            term_label = rows[0]["Term"]
            term = Term(
                term=term_label,
                chapter=rows[0]["Chapter"],
                new_member=True if rows[0]["New Member"] == "Y" else False,
                priv_gpa=(
                    float(rows[0]["Priv GPA"]) if rows[0]["Priv GPA"] else None
                ),
                priv_cum_gpa=(
                    float(rows[0]["Priv Cum GPA"])
                    if rows[0]["Priv Cum GPA"]
                    else None
                ),
                term_gpa=(
                    float(rows[0]["Term GPA"]) if rows[0]["Term GPA"] else None
                ),
                term_cum_gpa=(
                    float(rows[0]["Term Cum GPA"])
                    if rows[0]["Term Cum GPA"]
                    else None
                ),
            )
            # Add Course data to Term
            for row in rows:
                term.courses.append(
                    Course(
                        name=row["Class"],
                        catalog_number=row["Catalog No"],
                        hours=float(row["Hrs"]),
                        grade=Grade.from_string(row["Grade"]),
                    )
                )
            # Add Term to Member
            self.members[name].terms[term_label] = term
        return

    def add_grade_report_dir(self, grade_report_dir_path: str) -> None:
        """Add a directory of grade reports.

        Args:
            grade_report_dir_path (str): The path to the directory of grade
                reports.

        Raises:
            ValueError: Input path is not to a directory.

        Returns:
            None: None
        """
        if not os.path.isdir(grade_report_dir_path):
            raise ValueError("Path must be to directory.")
        for grade_report_path in os.listdir(grade_report_dir_path):
            if not grade_report_path.endswith(".csv"):
                continue
            self.add_grade_report(
                os.path.join(grade_report_dir_path, grade_report_path)
            )
