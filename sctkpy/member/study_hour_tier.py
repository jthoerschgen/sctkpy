"""Objects for organizing Study Hour Tier logic."""

from typing import Callable


class StudyHourTier:
    """Object for managing logic related to calculating what study hours a
    member would have."""

    def __init__(
        self,
        bound: float,
        condition: str,
        result_in_house: str = "",
        description_in_house: str = "",
        result_out_house: str = "",
        description_out_house: str = "",
    ):
        assert (
            bound >= 0.00 and bound <= 4.00
        ), "Threshold is for GPA, must be between 0.00-4.00"

        self.bound: float = bound
        self.condition: str = condition
        self.result_in_house: str = result_in_house
        self.description_in_house: str = description_in_house
        self.result_out_house: str = result_out_house
        self.description_out_house: str = description_out_house

        assert condition in (
            "<",
            "<=",
            "==",
            "!=",
            ">",
            ">=",
        ), "Invalid condition"

        compare_functions: dict[str, Callable[[float, float], bool]] = {
            "<": lambda x, y: x < y,
            "<=": lambda x, y: x <= y,
            "==": lambda x, y: x == y,
            "!=": lambda x, y: x != y,
            ">": lambda x, y: x > y,
            ">=": lambda x, y: x >= y,
        }
        self.compare: Callable[[float, float], bool] = compare_functions[
            condition
        ]

    def test_tier(self, gpa: float) -> bool:
        """Given a GPA as an input, will return a boolean value indicating if
        the StudyHourTier applies

        Args:
            gpa (float): GPA value between 0.00-4.00

        Returns:
            bool: If the tier applies to the given GPA
        """
        assert (
            gpa >= 0.00 and gpa <= 4.00
        ), f"GPA must be between 0.00-4.00, got: {gpa}"
        return self.compare(gpa, self.bound)


class StudyHourTierCumulative:
    """Object for managing logic related to calculating what study hours a
    member would have when both term and cumulative GPA numbers are required.
    """

    def __init__(
        self,
        term_bound: float,
        term_condition: str,
        cumulative_bound: float,
        cumulative_condition: str,
        result_in_house: str = "",
        description_in_house: str = "",
        result_out_house: str = "",
        description_out_house: str = "",
    ):
        self.term_condition = StudyHourTier(
            bound=term_bound,
            condition=term_condition,
        )
        self.cumulative_condition = StudyHourTier(
            bound=cumulative_bound,
            condition=cumulative_condition,
        )
        self.result_in_house: str = result_in_house
        self.description_in_house: str = description_in_house
        self.result_out_house: str = result_out_house
        self.description_out_house: str = description_out_house

    def test_tier(
        self,
        term_gpa: float,
        cumulative_gpa: float | None,
        on_social_probation: bool,
    ) -> bool:
        """Given a term and cumulative GPA as an input, will return a boolean
        value indicating if the ReduceStudyHourTier applies.

        Args:
            term_gpa (float): The term GPA being evaluated.
            cumulative_gpa (float | None): The cumulative GPA being evaluated.
            on_social_probation (bool): Social probation status.

        Returns:
            bool: _description_
        """
        assert (
            term_gpa >= 0.00 and term_gpa <= 4.00
        ), f"Term GPA must be between 0.00-4.00, got: {term_gpa}"
        assert cumulative_gpa is None or (
            cumulative_gpa >= 0.00 and cumulative_gpa <= 4.00
        ), f"Cumulative GPA must be between 0.00-4.00, got: {cumulative_gpa}"

        return (
            self.term_condition.compare(term_gpa, self.term_condition.bound)
            and (
                self.cumulative_condition.compare(
                    cumulative_gpa, self.cumulative_condition.bound
                )
                if cumulative_gpa is not None
                else True
            )
            and not on_social_probation
        )


class StrikeTier(StudyHourTier):
    """Object for managing logic related to strikes with added attribute for
    how many chances are permitted for that tier of strike.
    """

    def __init__(
        self,
        bound: float,
        condition: str,
        number_chances: int,
        result_in_house: str = "",
        description_in_house: str = "",
        result_out_house: str = "",
        description_out_house: str = "",
    ):
        super().__init__(
            bound,
            condition,
            result_in_house,
            description_in_house,
            result_out_house,
            description_out_house,
        )
        self.number_chances: int = number_chances
