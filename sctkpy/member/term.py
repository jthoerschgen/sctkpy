"""Objects needed for representing a Term at Missouri S&T"""

import re
from typing import Self

from sctkpy.member.course import Course


class Semester:
    """Representation of a Spring/Fall Semester.

    The specific purpose of this object is for better handling of determining
    previous semesters.

    Attributes:
        type (str): The type of term the semester is, either Spring (SP) or
            Fall (FS).
        year (int): The year the semester is from.
    """

    def __init__(self, term: str):
        assert re.match(
            r"^(FS|SP)\d{4}$", term
        ), f"Term must be in format 'SPXXXX' or 'FSXXXX', {term}"

        self.type: str = term[:2]
        self.year: int = int(term[2:])

    def __repr__(self) -> str:
        return f"{self.type}{self.year}"

    def __lt__(self, other: Self) -> bool:
        return not (self.type < other.type) and self.year < other.year

    def previous_semester(self) -> str:
        """Determine the previous semester of the semester object.

        Returns:
            str: The previous semester, as a string.
        """
        previous_semester: str = "SP" if self.type == "FS" else "FS"
        previous_year: int = self.year - 1 if self.type == "SP" else self.year
        return f"{previous_semester}{previous_year}"


class Term:
    """Representation of a term with associated course data.

    The hard-coded GPA information for the term is provided directly from the
    campus grade report csv file.

    The specific attributes are from the grade report csv file provided by
    Missouri S&T for the organization at midterms and finals.

    Attributes:
        term (Semester): The semester the term is from.
        chapter (str): The name of the chapter.
        new_member (bool): Is/Is not a pledge.
        priv_gpa (float): The term GPA of the member the previous term.
        priv_cum_gpa (float): The cumulative GPA of the member the previous
            term.
        term_gpa (float): The term GPA of the member for the term.
        term_cum_gpa (float): The cumulative GPA of the member for the term.
        courses (list[Course]): The courses the member is enrolled in for the
            term.
    """

    def __init__(
        self,
        term: str,
        chapter: str,
        new_member: bool,
        priv_gpa: float | None,
        priv_cum_gpa: float | None,
        term_gpa: float | None,
        term_cum_gpa: float | None,
        courses: list[Course] | None = None,
    ):
        self.term: Semester = Semester(term)
        self.chapter: str = chapter
        self.new_member: bool = new_member
        self.priv_gpa: float | None = priv_gpa
        self.priv_cum_gpa: float | None = priv_cum_gpa
        self.term_gpa: float | None = term_gpa
        self.term_cum_gpa: float | None = term_cum_gpa
        self.courses: list[Course] = courses if courses is not None else []

    def calculate_gpa(self) -> float | None:
        """Calculates the GPA of all the courses for the term.

        Returns:
            float | None: The GPA if it exists, otherwise None.
        """
        grade_points: float = 0.0
        hours: float = 0.0
        for course in self.courses:
            if course.grade is None or course.grade.value is None:
                continue
            grade_points += course.grade.value * course.hours
            hours += course.hours
        gpa: float | None = grade_points / hours if hours != 0 else None
        return gpa
