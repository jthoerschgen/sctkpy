"""Object for representing a student at Missouri S&T for grade evaluation."""

from dataclasses import dataclass

from sctkpy.config import (
    academic_suspension_cumulative,
    academic_suspension_term,
    get_off_no_punting,
    get_off_social_probation,
    no_punting,
    no_study_hours,
    reduce_one_tier,
    reduce_two_tiers,
    social_probation,
    tier_one,
    tier_two,
)
from sctkpy.member.study_hour_tier import StudyHourTier
from sctkpy.member.term import Semester, Term


@dataclass
class GradeReportItem:
    """Class for keeping track of a row for the Grade Report"""

    def __init__(
        self,
        name: str,
        out_of_house: bool,
        pledge_class: str | None,
        cumulative_gpa: float | None,
        previous_term: str | None,
        previous_gpa: float | None,
        term: str,
        term_gpa: float | None,
        study_hours: str,
    ):
        self.name: str = name
        self.out_of_house: bool = out_of_house
        self.pledge_class: str | None = pledge_class
        self.cumulative_gpa: float | None = cumulative_gpa
        self.previous_term: str | None = previous_term
        self.previous_gpa: float | None = previous_gpa
        self.term: str = term
        self.term_gpa: float | None = term_gpa
        self.study_hours: str = study_hours


class Member:
    """Representation of a member who is a student enrolled at Missouri S&T.

    The primary purpose of the methods for a Member is to determine what
    academic probation they have using the grade data in the 'terms' attribute.

    Attributes:
        name (str): The first and last name of the member as one string.
        out_of_house (bool): The in/out of house status for the member, as a
            boolean value. True for out-of-house status.
        terms (dict[str, Term]): A collection of grade data for the member
            stored in a dictionary where the key is the name of the term, and
            the value is the associated Term object.
    """

    def __init__(
        self,
        name: str,
        out_of_house: bool,
        terms: dict[str, Term] | None = None,
    ):
        self.name: str = name
        self.out_of_house: bool = out_of_house
        self.terms: dict[str, Term] = terms if terms is not None else dict()

    def get_pledge_class(self) -> str | None:
        """Returns the term the Member was a 'New Member' if it exists.

        Returns:
            str | None: The term the Member was a 'New Member' if it exists,
                else None.
        """
        for key, term in self.terms.items():
            if term.new_member:
                return key
        return None

    def get_next_previous_term(self, selected_term: str) -> str | None:
        """Given a selected term, determine the next previous term which the
        member has grade data for.

        Args:
            selected_term (str): The term that a previous term is being
                searched for.

        Returns:
            str | None: The next previous term if it exists, will return None
                if no previous term exists.
        """

        def sort_key(term: str) -> tuple[int, int]:
            """Function used for sorting terms.

            Terms are in the format: FSXXXX or SPXXXX; where the first two
            characters in the string are either SP or FS (for Spring and Fall)
            and the last four characters represent a four digit year.

            Gives the term from a list a number value used for sorting.

            Args:
                term (str): The term being evaluated for sorting.

            Returns:
                tuple[int, int]: The sorting value for the term.
            """
            term_year: int = int(term[2:])
            term_semester_order: int = 0 if term[:2] == "SP" else 1
            return (term_year, term_semester_order)

        terms: list[str] = sorted(list(self.terms.keys()), key=sort_key)

        if (len(terms) == 0) or (selected_term == terms[0]):
            return None

        previous_term: str = Semester(selected_term).previous_semester()

        if Semester(previous_term) < Semester(terms[0]):
            return None

        previous_gpa: float | None = None
        if previous_term in terms:
            previous_gpa = self.terms[previous_term].calculate_gpa()

        while (
            (previous_term not in terms) and (previous_term != terms[0])
        ) or (previous_gpa is None):
            previous_term = Semester(previous_term).previous_semester()

            if previous_term in terms:
                previous_gpa = self.terms[previous_term].calculate_gpa()

        return previous_term

    def is_on_social_probation(self, selected_term: str) -> bool:
        """Given a term, determine if the member shall be on social probation
        due to their academics.

        Args:
            selected_term (str): The term which is being tested.

        Raises:
            ValueError: If the current GPA is None.

        Returns:
            bool: Is the member on social probation?
        """
        current_term: str = selected_term
        current_gpa: float | None = self.terms[current_term].calculate_gpa()
        previous_term: str | None = self.get_next_previous_term(current_term)

        if current_gpa is None:
            raise ValueError("GPA cannot be none")

        if previous_term is None and social_probation.test_tier(current_gpa):
            return True

        while previous_term is not None:
            previous_gpa: float | None = self.terms[
                previous_term
            ].calculate_gpa()

            if not (previous_gpa is None or current_gpa is None):
                if get_off_social_probation.test_tier(current_gpa):
                    return False
                if social_probation.test_tier(
                    previous_gpa
                ) or social_probation.test_tier(current_gpa):
                    return True

            current_term = previous_term
            current_gpa = self.terms[current_term].calculate_gpa()
            previous_term = self.get_next_previous_term(current_term)

        return False

    def is_on_no_punting(self, selected_term: str) -> bool:
        """Given a term, determine if the member shall be on no punting due to
        their academics.

        Args:
            selected_term (str): The term which is being tested.

        Raises:
            ValueError: If the current GPA is None.

        Returns:
            bool: Is the member on no punting?
        """
        current_term: str = selected_term
        current_gpa: float | None = self.terms[current_term].calculate_gpa()
        previous_term: str | None = self.get_next_previous_term(current_term)

        if current_gpa is None:
            raise ValueError("GPA cannot be none")

        if previous_term is None and no_punting.test_tier(current_gpa):
            return True

        while previous_term is not None:
            previous_gpa: float | None = self.terms[
                previous_term
            ].calculate_gpa()

            if not (previous_gpa is None or current_gpa is None):
                if get_off_no_punting.test_tier(current_gpa):
                    return False
                if no_punting.test_tier(previous_gpa) or no_punting.test_tier(
                    current_gpa
                ):
                    return True

            current_term = previous_term
            current_gpa = self.terms[current_term].calculate_gpa()
            previous_term = self.get_next_previous_term(current_term)

        return False

    def determine_study_hours(
        self, selected_term: str, on_social_probation: bool
    ) -> StudyHourTier:
        """Determine the amount of study hours a member has for a selected
        term.

        Args:
            selected_term (str): The term which is being tested.
            on_social_probation (bool): Is the member on social probation for
                the selected term.

        Raises:
            ValueError: If the current GPA is None.

        Returns:
            StudyHourTier: The study hours the member shall have for the
                selected term.
        """
        current_term: str = selected_term
        current_gpa: float | None = self.terms[current_term].calculate_gpa()
        previous_term: str | None = self.get_next_previous_term(current_term)

        if current_gpa is None:
            raise ValueError("GPA cannot be none")

        cumulative_gpa = self.terms[current_term].term_cum_gpa

        study_hour_tier: int | None = None

        if previous_term is None:
            if tier_two.test_tier(current_gpa):
                study_hour_tier = 2
            elif tier_one.test_tier(current_gpa):
                study_hour_tier = 1
            else:
                study_hour_tier = 0

        while previous_term is not None:
            previous_gpa: float | None = self.terms[
                previous_term
            ].calculate_gpa()
            if previous_gpa is None or current_gpa is None:
                current_term = previous_term
                current_gpa = self.terms[current_term].calculate_gpa()
                previous_term = self.get_next_previous_term(current_term)
                continue

            if tier_two.test_tier(previous_gpa):
                if reduce_two_tiers.test_tier(
                    current_gpa, cumulative_gpa, on_social_probation
                ):
                    study_hour_tier = 0
                    break
                elif reduce_one_tier.test_tier(
                    current_gpa, cumulative_gpa, on_social_probation
                ):
                    study_hour_tier = 1
                else:
                    study_hour_tier = 2
                    break
            elif tier_one.test_tier(previous_gpa):
                if reduce_one_tier.test_tier(
                    current_gpa, cumulative_gpa, on_social_probation
                ):
                    study_hour_tier = 0
                    break
                elif tier_two.test_tier(current_gpa):
                    study_hour_tier = 2
                    break
                else:
                    study_hour_tier = 1
            else:
                if tier_two.test_tier(current_gpa):
                    study_hour_tier = 2
                    break
                elif tier_one.test_tier(current_gpa):
                    study_hour_tier = 1
                    break
                else:
                    study_hour_tier = 0
                    break

            current_term = previous_term
            current_gpa = self.terms[current_term].calculate_gpa()
            previous_term = self.get_next_previous_term(current_term)

        if study_hour_tier not in (0, 1, 2):
            raise ValueError(
                f"Study hour tier for {self.name} {selected_term} is "
                + f"{study_hour_tier}, must be either 0, 1, or 2."
            )

        if study_hour_tier == 2:
            return tier_two
        elif study_hour_tier == 1:
            return tier_one
        else:  # study_hour_tier == 0:
            return no_study_hours

    def is_on_suspension(self, selected_term: str) -> bool:
        """Given a term, determine if the member shall be on academic
        suspension due to their academics.

        Args:
            selected_term (str): The term which is being tested.

        Raises:
            ValueError: If the current GPA is None.

        Returns:
            bool: Is the member on academic suspension?
        """
        current_term: str = selected_term
        current_gpa: float | None = self.terms[current_term].calculate_gpa()

        cumulative_gpa: float | None = self.terms[current_term].term_cum_gpa

        if current_gpa is None:
            raise ValueError("GPA cannot be none")

        if self.terms[current_term].new_member:
            return False  # New members cannot be on suspension.
        if academic_suspension_term.test_tier(current_gpa):
            return True
        if cumulative_gpa is not None:
            if academic_suspension_cumulative.test_tier(cumulative_gpa):
                return True
        return False

    def determine_academic_probation(
        self, selected_term: str
    ) -> GradeReportItem:
        """Determine a Member's academic probation for a selected semester.

        The metrics used for evaluating a Member's academic probation are
        outlined in the Scholarship Policy. If any changes are made to the
        policy, this method may become outdated.

        Args:
            selected_term (str): The term the member is being evaluated for.

        Returns:
            GradeReportItem: Dataclass of information used by the grade report.
        """
        current_term: str = selected_term

        current_gpa: float | None = None
        if current_term in self.terms:
            current_gpa = self.terms[current_term].calculate_gpa()

        while current_gpa is None:
            previous_term: str | None = self.get_next_previous_term(
                current_term
            )
            if previous_term is None:
                return GradeReportItem(
                    name=self.name,
                    out_of_house=self.out_of_house,
                    pledge_class=self.get_pledge_class(),
                    cumulative_gpa=None,
                    previous_term=None,
                    previous_gpa=None,
                    term=current_term,
                    term_gpa=None,
                    study_hours="",
                )

            current_term = previous_term
            current_gpa = self.terms[current_term].calculate_gpa()

        cumulative_gpa: float | None = self.terms[current_term].term_cum_gpa

        on_no_punting: bool = self.is_on_no_punting(current_term)
        on_social_probation: bool = self.is_on_social_probation(current_term)
        on_suspension: bool = self.is_on_suspension(current_term)

        study_hours = self.determine_study_hours(
            current_term, on_social_probation
        )

        results: list[StudyHourTier] = []

        results.append(study_hours)
        if on_no_punting:
            results.append(no_punting)
        if on_social_probation:
            results.append(social_probation)
        if on_suspension:
            results.append(academic_suspension_term)

        # Output Final Result
        result_outcomes: list[str] = []
        for result in results:
            result_outcomes.append(
                result.result_out_house
                if self.out_of_house
                else result.result_in_house
            )
        result_str: str = " ".join(result_outcomes)

        previous_term = self.get_next_previous_term(current_term)
        previous_gpa: float | None = (
            self.terms[previous_term].calculate_gpa()
            if previous_term is not None
            else None
        )

        return GradeReportItem(
            name=self.name,
            out_of_house=self.out_of_house,
            pledge_class=self.get_pledge_class(),
            cumulative_gpa=cumulative_gpa,
            previous_term=previous_term,
            previous_gpa=previous_gpa,
            term=current_term,
            term_gpa=current_gpa,
            study_hours=result_str,
        )
