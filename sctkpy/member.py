# -*- coding: utf-8 -*-\

"""Member data objects defined here
"""

import logging
import re
import sqlite3

from .config import (
    StudyHourTier,
    gpa_map,
    no_punting,
    no_study_hours,
    reduce_no_punting,
    reduce_one_tier,
    reduce_social_probation,
    reduce_two_tiers,
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
        """Gather grade data from SQLite and parse into objects.

        Raises:
            AssertionError: Multi-valued data is not redundant as expected.
            ValueError: 'new_member' value in DB is neither 'Y'/'N'.
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
            ]  # Values in columns should be the same for the same member.
            try:
                for column in single_value_column_names:
                    assert (
                        len({row[column] for row in rows}) == 1
                    ), f"error in column: {column}"
            except AssertionError as exc:
                logger.error(
                    "%s: "
                    + "Parent of multi-valued data is not "
                    + "redundant as expected",
                    exc,
                )
                logger.error("\tError in data for %s:", self.name)
                for column in single_value_column_names:
                    logger.error(
                        "\t\t%s: %s",
                        column,
                        ",".join([str(row[column]) for row in rows]),
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

    def get_previous_term(self, selected_term: str) -> str | None:
        """Given a term in a format SPXXXX or FSXXXX, (e.g. FS2021, SP2022)
        return the previous term if it exists

        Args:
            selected_term (str): Term to find the term before.

        Returns:
            str | None: If previous term exists return it, else None.
        """
        logger.debug("Getting previous term for %s...", selected_term)
        term_list = sorted(
            [term for term in self.terms.keys()],
            key=lambda term: (
                int(term[2:]),
                0 if term[:2] == "SP" else 1,
            ),
        )  # Sort list by year and then by term, (SP before FS).
        logger.debug("Terms: %s", term_list)
        if len(term_list) == 0:
            logger.debug("Cannot get previous term for %s", selected_term)
            return None
        if selected_term == term_list[0]:  # First term has no previous term.
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

    def calculate_gpa(self, terms: list[Term]) -> float | None:
        """Calculates GPA of a list of terms.

        Args:
            terms (list[Term]): list of terms to calculate GPA from.

        Returns:
            float | None: GPA value if GPA can be calculated, else None.
        """
        logger.debug(
            "Calculating %s's GPA for: %s",
            self.name,
            [term.term for term in terms],
        )
        sum_points = 0
        sum_credits = 0
        for term in terms:
            for course in term.classes:
                grade_point: int | None = gpa_map[course.grade]
                if grade_point is not None:
                    sum_points += grade_point * course.hrs
                    sum_credits += course.hrs

                    logger.debug(
                        '\t\tCourse Info: %s %s %s, %i hrs, grade="%s", '
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
                else:
                    logger.warning(
                        '\t\tCannot use course: %s %s %s, %i hrs, grade="%s"',
                        term.term,
                        course.class_name,
                        course.catalog_no,
                        course.hrs,
                        course.grade,
                    )

        if sum_credits == 0:
            logger.warning(
                "\t%s is in 0 credit hours, unable to calculate GPA", self.name
            )
            return None

        gpa: float = sum_points / sum_credits
        logger.debug(
            "\t%s's GPA = %i / %i = (sum grade points / sum credit hrs) = %f",
            self.name,
            sum_points,
            sum_credits,
            gpa,
        )

        return gpa

    def get_next_previous_gpa_and_term(
        self, selected_term: str | None
    ) -> tuple[float | None, str | None]:
        """From a previous term, get the next previous available GPA and term.

        Args:
            selected_term (str | None):
                Previous term to get next previous gpa and term from.

        Returns:
            tuple[float | None, str | None]:
                Previous GPA and term if available.
        """
        previous_term: str | None = selected_term
        previous_gpa: float | None = None

        while previous_gpa is None and previous_term is not None:
            print(previous_term, previous_gpa)
            previous_gpa = self.calculate_gpa(
                terms=[self.terms[previous_term]]
            )
            if previous_gpa is None:
                previous_term = self.get_previous_term(previous_term)
        return previous_gpa, previous_term

    def study_hours(
        self, selected_term: str
    ) -> tuple[tuple[str, float | None], tuple[str | None, float | None], str]:
        """Calculate GPA and Study Hours status for a member in a given term.

        Args:
            selected_term (str): Term to calculate study hour status from.

        Returns:
            tuple[
                tuple[str, float | None], tuple[str | None, float | None], str
            ]:
                First tuple[str, float | None]: selected term and GPA.
                First tuple[str, float | None]: previous term and GPA.
                str: Study Hours outcome for the selected term.
        """
        logger.debug("%s", "~" * 50)
        logger.debug(
            "Calculating Grade Info for: %s (Out of House: %s) (Term: %s)",
            self.name,
            "Yes" if self.out_of_house else "No",
            selected_term,
        )
        logger.debug("%s", "~" * 50)

        previous_term: str | None = self.get_previous_term(selected_term)
        while previous_term is not None and (
            selected_term not in self.terms.keys()
        ):  # If the selected term is unavailable, search backwards for
            # available term.
            logging.debug(
                "\tCan't find the selected term: %s, getting previous term...",
                selected_term,
            )
            selected_term = previous_term
            previous_term = self.get_previous_term(selected_term)
        if selected_term not in self.terms.keys():
            return ((selected_term, None), (previous_term, None), "")

        # Find the GPA of the selected term.
        current_gpa: float | None = self.calculate_gpa(
            terms=[self.terms[selected_term]]
        )
        if current_gpa is None and previous_term is not None:
            return self.study_hours(previous_term)

        logger.debug(
            "\t\tCurrent Term:  %s, GPA: %f", selected_term, current_gpa
        )

        assert (
            current_gpa is not None
        )  # GPA should never be None past this point.

        # Find the GPA of the previous term. If the previous term does not
        # have a GPA, then search backwards for previous term with a GPA.
        previous_gpa, previous_term = self.get_next_previous_gpa_and_term(
            previous_term
        )

        # Calculate Study Hour Tier.
        # Method for determining Study Hour Tier:
        #   -   Study hour tier is represented as a score.
        #   -   Using previous data, determine if the member was previously on
        #       study hours and try to reduce study hours based off the current
        #       term.
        #   -   Break when study hours cannot be reduced further, or if study
        #       hours are completely reduced.
        logger.debug("Determining # Study Hours...")
        tier: int = (
            0  # Study hour tier of the previous term, to be calculated.
        )

        # Create copies of values for use in the loop.
        current_gpa_copy = current_gpa
        previous_gpa_copy = previous_gpa
        previous_term_copy = previous_term
        while previous_term_copy is not None:
            logger.debug(
                "\t\tPrevious Term: %s, GPA: %s",
                previous_term_copy,
                previous_gpa_copy,
            )
            if previous_gpa_copy is None:  # No previous GPA available.
                break

            logger.debug("\t\t\tStarting Tier: %i", tier)
            if tier_two.test_tier(
                previous_gpa_copy
            ):  # Previously had tier two.
                if reduce_two_tiers.test_tier(
                    current_gpa_copy
                ):  # Can reduce two tiers from tier two, now no study hours.
                    tier = 0
                    break
                elif reduce_one_tier.test_tier(
                    current_gpa_copy
                ):  # Can reduce one tier from tier two, now tier one.
                    tier = 1

                else:  # Cannot reduce, still one tier two.
                    tier = 2
                    break

            elif tier_one.test_tier(
                previous_gpa_copy
            ):  # Previously had tier one.
                if reduce_one_tier.test_tier(
                    current_gpa_copy
                ):  # Can reduce one tier from tier one, now no study hours.
                    tier = 0
                    break
                elif tier_two.test_tier(
                    current_gpa_copy
                ):  # GPA declined from tier one to tier two, now tier two.
                    tier = 2
                    break
                else:  # Cannot reduce, GPA still at tier one, still tier one.
                    tier = 1

            else:  # Ignoring previous semesters, would have no study hours.
                if tier_two.test_tier(
                    current_gpa_copy
                ):  # GPA declined to tier two, now tier two.
                    tier = 2
                    break
                elif tier_one.test_tier(
                    current_gpa_copy
                ):  # GPA declined to tier one, now tier one.
                    tier = 1
                    break
                else:  # GPA still doesn't require study hours, no study hours.
                    tier = 0
                    break

            logger.debug("\t\t\tEnding Tier: %i", tier)

            current_gpa_copy = previous_gpa_copy
            previous_term_copy = self.get_previous_term(previous_term_copy)
            previous_gpa_copy, previous_term_copy = (
                self.get_next_previous_gpa_and_term(previous_term_copy)
            )

        logger.debug("\t\t\tFINAL Tier: %i", tier)

        assert tier >= 0 and tier <= 2, tier

        outcomes: list[StudyHourTier] = []

        # Based off the tier of study hours from the previous semester,
        # attempt to reduce and assign appropriate outcome.
        if tier == 2 or tier_two.test_tier(current_gpa):
            if reduce_two_tiers.test_tier(current_gpa):
                outcomes.append(no_study_hours)
            elif reduce_one_tier.test_tier(current_gpa):
                outcomes.append(tier_one)
            else:
                outcomes.append(tier_two)
        elif tier == 1 or tier_one.test_tier(current_gpa):
            if reduce_one_tier.test_tier(current_gpa):
                outcomes.append(no_study_hours)
            else:
                outcomes.append(tier_one)
        else:
            outcomes.append(no_study_hours)

        # Determine punting privileges.
        logger.debug("Determining Punting Privileges...")
        if previous_gpa is None and no_punting.test_tier(current_gpa):
            outcomes.append(no_punting)

        current_gpa_copy = current_gpa
        previous_gpa_copy = previous_gpa
        previous_term_copy = previous_term
        while previous_term_copy is not None:
            logger.debug(
                "\t\tPrevious Term: %s, GPA: %s",
                previous_term_copy,
                previous_gpa_copy,
            )
            if previous_gpa_copy is None:
                break

            if reduce_no_punting.test_tier(current_gpa_copy):
                break
            elif no_punting.test_tier(current_gpa_copy):
                outcomes.append(no_punting)
                break

            current_gpa_copy = previous_gpa_copy
            previous_term_copy = self.get_previous_term(previous_term_copy)
            previous_gpa_copy, previous_term_copy = (
                self.get_next_previous_gpa_and_term(previous_term_copy)
            )

        # Determine social probation status.
        logger.debug("Determining Social Probation Status...")
        if social_probation.test_tier(current_gpa):
            outcomes.append(social_probation)

        outcome_results: list[str] = [
            (
                outcome.result_out_house
                if self.out_of_house
                else outcome.result_in_house
            )
            for outcome in outcomes
        ]
        result: str = " ".join(outcome_results)

        return (
            (selected_term, current_gpa),
            (previous_term, previous_gpa),
            result,
        )

    def generate_academic_report(
        self,
    ) -> tuple[list[str], list[float | None], list[float | None]]:
        """Get term and cumulative GPA for each term.

        Returns:
            tuple[list[str], list[float | None], list[float | None]]:
                tuple of lists of: terms, term gpa's, and cumulative gpa's
        """
        terms = sorted(
            list(self.terms.keys()),
            key=lambda term: (
                int(term[2:]),
                0 if term[:2] == "SP" else 1,
            ),
        )  # Sort terms in chronological order.

        term_gpas = [self.calculate_gpa([self.terms[term]]) for term in terms]

        cumulative_gpas = [
            self.calculate_gpa([self.terms[term] for term in terms[: i + 1]])
            for i in range(len(terms))
        ]

        return terms, term_gpas, cumulative_gpas
