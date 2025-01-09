"""Utility methods and objects used by tests."""

from sctkpy.member.course import Course, Grade
from sctkpy.member.term import Term

gpa_presets: dict[str, list[Grade]] = {
    "2.00": [Grade.C] * 4,
    "2.50": [Grade.B] * 2 + [Grade.C] * 2,
    "2.60": [Grade.B] * 3 + [Grade.C] * 2,
    "2.75": [Grade.B] * 3 + [Grade.C],
    "3.00": [Grade.B] * 4,
    "3.25": [Grade.A] + [Grade.B] * 3,
    "3.50": [Grade.A] * 2 + [Grade.B] * 2,
}


def generate_example_term(
    grades: list[Grade],
    term_cumulative_gpa: float = 0.00,
    term: str = "FS2024",
) -> Term:
    """Generate an example Term object used for testing grade evaluation.

    Args:
        grades (list[Grade]): a list of grades for the term.
        term_cumulative_gpa (float, optional): A preset for the cumulative GPA
            of the member at that term. Defaults to 0.00.
        term (str, optional): The label for the term. Defaults to "FS2024".

    Returns:
        Term: A valid term object that uses the argument values.
    """
    return Term(
        term=term,
        chapter="Beta Sigma Psi",
        new_member=False,
        priv_gpa=0.00,
        priv_cum_gpa=0.00,
        term_gpa=0.00,
        term_cum_gpa=term_cumulative_gpa,
        courses=[
            Course(
                name="Test_Course",
                catalog_number="1001",
                hours=3,
                grade=grade,
            )
            for grade in grades
        ],
    )


def generate_example_terms(
    input_terms: dict[str, list[Grade]], term_cumulative_gpa: float
) -> dict[str, Term]:
    """Generate a dictionary of example terms appropriate for a Member object.

    Args:
        input_terms (dict[str, list[Grade]]): A dictionary of terms and grades.
        term_cumulative_gpa (float): The cumulative GPA of the member.

    Returns:
        dict[str, Term]: A list of terms valid for a Member object.
    """
    example_terms = {}
    for term, grades in input_terms.items():
        example_terms[term] = generate_example_term(
            grades, term_cumulative_gpa, term
        )
    return example_terms
