"""Objects needed for representing a course at Missouri S&T."""

from enum import Enum
from typing import Self


class Grade(Enum):
    """Enum for Grades

    Names are the letter Grade, values are the amount of grade points each
    letter grade is worth.
    """

    A = 4
    B = 3
    C = 2
    D = 1
    F = 0

    @classmethod
    def from_string(cls, grade: str) -> Self | None:
        """Get a Grade from a letter grade as a string.

        Matches the input letter grade to the Enum, if the letter grade is not
        A, B, C, D, or F, returns None.

        Args:
            grade (str): The letter grade.

        Returns:
            Self | None: The corresponding Grade or None.
        """
        return cls.__members__.get(grade.upper(), None)


class Course:
    """Representation of an individual course at Missouri S&T.

    Courses are collected into terms. The course data is for a student/member.
    The main purpose of the course object is to calculate the member's GPA for a
    given term, which requires the hours and grade data of the course.

    The specific attributes are from the grade report CSV file provided by
    Missouri S&T for the organization at midterms and finals.

    Attributes:
        name (str): The name of the course.
        catalog_number (str): The catalog number for the course.
        hours (float): The number of credit hours the course is worth.
        grade (Grade | None): The letter grade in the course.
    """

    def __init__(
        self, name: str, catalog_number: str, hours: float, grade: Grade | None
    ):
        self.name: str = name
        self.catalog_number: str = catalog_number
        self.hours: float = hours
        self.grade: Grade | None = grade
