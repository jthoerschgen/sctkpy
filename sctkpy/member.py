# -*- coding: utf-8 -*-\

"""Member data objects defined here
"""

import logging
import re
import sqlite3

from .config import (
    FULL_TIME_HOURS,
    gpa_map,
    no_punting,
    no_study_hours,
    social_probation,
    tier_one,
    tier_two,
)
from .db_funcs import create_db_conn

logger = logging.getLogger(__name__)


class Class:
    """Structures the data for class/course information"""

    def __init__(
        self, class_name: str, catalog_no: str, hrs: int, grade: str
    ) -> None:
        self.class_name: str = class_name
        self.catalog_no: str = catalog_no
        self.hrs: int = hrs
        self.grade: str = grade


class Term:
    """Structures the data for academic term information"""

    def __init__(
        self,
        term: str,
        chapter: str,
        new_member: bool,
        priv_gpa: float,
        priv_cum_gpa: float,
        term_gpa: float,
        term_cum_gpa: float,
        classes: list[Class] | None = None,
    ) -> None:
        self.term: str = term
        self.chapter: str = chapter
        self.new_member: bool = new_member
        self.priv_gpa: float = priv_gpa
        self.priv_cum_gpa: float = priv_cum_gpa
        self.term_gpa: float = term_gpa
        self.term_cum_gpa: float = term_cum_gpa
        self.classes: list[Class] = classes if classes is not None else []

        assert re.match(
            r"^(FS|SP)\d{4}$", self.term
        ), "Term must be in format 'SPXXXX' or 'FSXXXX'"


class Member:
    """Structures the data for member academic information"""

    def __init__(
        self,
        name: str,
        out_of_house: bool,
        terms: dict[str, Term] | None = None,
    ) -> None:
        self.name: str = name
        self.out_of_house: bool = out_of_house
        self.terms: dict[str, Term] = terms if terms is not None else {}

        if terms is None:  # if no term data is provided in constructor
            self.import_grades()

        self.pledge_class: str | None = (
            [sem for sem, term in self.terms.items() if term.new_member][0]
            if len(self.terms.keys()) > 0
            else None
        )

    def import_grades(self):
        """Gather grade data from SQLite and parse into objects

        Raises:
            AssertionError: Multi-valued data is not redundant as expected
            ValueError: 'new_member' value in DB is neither 'Y'/'N'
        """
        logger.debug("Importing grade data for: %s", self.name)
        conn = create_db_conn()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM grades WHERE name = ?", (self.name,))
        rows = cur.fetchall()

        rows_by_term = {}
        term = ""
        for row in rows:
            if row["term"] != term:
                rows_by_term[row["term"]] = []
            rows_by_term[row["term"]].append(row)
            term = row["term"]

        for term, rows in rows_by_term.items():
            logger.debug("\tAdding Data from: %s", term)
            single_value_column_names = [
                "term",
                "chapter",
                "new_member",
                "priv_gpa",
                "priv_cum_gpa",
                "term_gpa",
                "term_cum_gpa",
            ]  # Values in these columns should be the same for the same member
            try:
                for column in single_value_column_names:
                    assert (
                        len({row[column] for row in rows}) == 1
                    ), f"error in column: {column}"
            except AssertionError as exc:
                logger.error(
                    "Parent of multi-valued data is not redundant as expected"
                )
                raise exc

            if rows[0]["new_member"] == "Y":
                is_new_member = True
            elif rows[0]["new_member"] == "N":
                is_new_member = False
            else:
                raise ValueError(
                    "From DB col value 'new_member' is not 'Y'/'N'",
                    rows[0]["new_member"],
                )

            term = Term(
                term=rows[0]["term"],
                chapter=rows[0]["chapter"],
                new_member=is_new_member,
                priv_gpa=rows[0]["priv_gpa"],
                priv_cum_gpa=rows[0]["priv_cum_gpa"],
                term_gpa=rows[0]["term_gpa"],
                term_cum_gpa=rows[0]["term_cum_gpa"],
                classes=[
                    Class(
                        class_name=row["class"],
                        catalog_no=row["catalog_num"],
                        hrs=row["hrs"],
                        grade=row["grade"],
                    )
                    for row in rows
                ],
            )
            self.terms[rows[0]["term"]] = term

            # logging
            logger.debug("\tTerm Data:")
            for key, val in term.__dict__.items():
                if isinstance(val, list):
                    logger.debug("\t\t%s:", key)
                    for item in val:
                        if isinstance(item, Class):
                            logger.debug("\t\t\t%s", item.__dict__)
                else:
                    logger.debug("\t\t%s: %s", key, val)
        return

    def get_prev_term(self, selected_term: str) -> str | None:
        """Given a term in a format SPXXXX or FSXXXX, (e.g. FS2021, SP2022)
        return the previous term if it exists

        Args:
            selected_term (str): Term to find the term before

        Returns:
            str | None: If previous term exists return it, else None
        """
        logger.debug("Getting previous term for %s...", selected_term)
        term_list = sorted(
            [term for term in self.terms.keys()],
            key=lambda term: (
                (
                    (int(term[2:])),
                    (not term[:2]),
                ),
            ),
        )  # Sort list by year and then by term, (SP before FS)
        logger.debug("Terms: %s", term_list)
        if len(term_list) == 0:
            logger.debug("Cannot get previous term for %s", selected_term)
            return None
        while int(selected_term[2:]) > int(term_list[0][2:]) and not (
            selected_term[:2] < term_list[0][:2]
        ):
            if selected_term[:2] == "FS":
                selected_term = "SP" + selected_term[2:]
            else:
                selected_term = "FS" + str(int(selected_term[2:]) - 1)
            if selected_term in term_list:
                break
        logger.debug("Previous term is: %s", selected_term)
        return selected_term if selected_term in term_list else None

    def study_hours(self, selected_term: str) -> tuple[str, float | None, str]:
        """Calculate GPA and Study Hours status for a member in a given term

        Args:
            selected_term (str): Term to calculate study hour status from

        Returns:
            tuple[float | None, str]:
                Tuple of (GPA, Study Hour Status) or (None, Empty String) if
                member does not have sufficient data for the input term.
        """
        logger.debug("%s", "~" * 50)
        logger.debug(
            "Calculating Grade Info for: %s (Out of House: %s) (Term: %s)",
            self.name,
            "Yes" if self.out_of_house else "No",
            selected_term,
        )
        logger.debug("%s", "~" * 50)

        if selected_term not in self.terms.keys():
            logger.warning(
                "%s has no data for term: %s", self.name, selected_term
            )

            previous_term = self.get_prev_term(selected_term=selected_term)
            logger.warning("Using previous term: %s", previous_term)

            if previous_term is not None:
                return self.study_hours(previous_term)

            else:  # If no previous term exists, member must be new
                logger.debug("\t%s is a new member", self.name)
                outcomes = [tier_two, no_punting]  # Pledges shall study

                # Combine study hour restrictions into a single string
                result = " ".join(
                    [
                        (
                            outcome.result_out_house
                            if self.out_of_house
                            else outcome.result_in_house
                        )
                        for outcome in outcomes
                    ]
                )
                return (selected_term, None, result)

        terms = [self.terms[selected_term]]
        sum_points = 0
        sum_credits = 0
        for term in terms:
            for course in term.classes:
                grade_point: int | None = gpa_map[course.grade]
                if grade_point is not None:
                    sum_points += grade_point * course.hrs
                    sum_credits += course.hrs

                    logger.debug(
                        '\t\tCourse Info: %s %s %s, %i hrs, grade = "%s", '
                        + "(grade point: %s, weight (grade point x hrs): %s)",
                        term.term,
                        course.class_name,
                        course.catalog_no,
                        course.hrs,
                        course.grade,
                        str(grade_point),
                        (
                            str(grade_point * course.hrs)
                            if grade_point is not None
                            else "None"
                        ),
                    )
            if (
                sum_credits < FULL_TIME_HOURS
            ):  # if member has less that full-time status, use previous
                # semester grade data until they have enough hrs to be
                logger.warning(
                    "\t%s is in < %i credit hours (%i), "
                    + "trying to add previous term.",
                    self.name,
                    FULL_TIME_HOURS,
                    sum_credits,
                )

                previous_term = self.get_prev_term(selected_term=term.term)
                logger.warning("Using previous term: %s", previous_term)

                if previous_term is not None:
                    terms.append(self.terms[previous_term])
                else:
                    logger.warning("Previous term does not exist")
                    break

        if sum_credits == 0:
            logger.warning(
                "\t%s is in 0 credit hours, unable to calculate GPA", self.name
            )
            return (selected_term, None, "")

        gpa: float = sum_points / sum_credits
        logger.debug(
            "\t%s's GPA = %i / %i = (sum grade points / sum credit hrs) = %f",
            self.name,
            sum_points,
            sum_credits,
            gpa,
        )

        outcomes = []
        if no_study_hours.test_tier(gpa):
            outcomes.append(no_study_hours)
        elif tier_one.test_tier(gpa) and not tier_two.test_tier(gpa):
            outcomes.append(tier_one)
        elif tier_two.test_tier(gpa):
            outcomes.append(tier_two)

        if no_punting.test_tier(gpa):
            outcomes.append(no_punting)

        if len(terms) == 1 and terms[0].new_member:  # Pledges shall study
            logger.debug("\t%s is a new member", self.name)
            outcomes = [tier_two, no_punting]

        if social_probation.test_tier(gpa):
            outcomes.append(social_probation)

        for outcome in outcomes:
            logger.debug(
                "\t%s has a GPA %s %f: %s",
                self.name,
                outcome.condition,
                outcome.bound,
                (
                    outcome.result_out_house
                    if self.out_of_house
                    else outcome.result_in_house
                ),
            )

        # Combine study hour restrictions into a single string
        result = " ".join(
            [
                (
                    outcome.result_out_house
                    if self.out_of_house
                    else outcome.result_in_house
                )
                for outcome in outcomes
            ]
        )
        logger.debug(
            "\t%s, GPA: %.3f, Outcome: %s",
            self.name,
            gpa,
            result if result != "" else "No Study Hours",
        )
        return ([term.term for term in terms][-1], gpa, result)
