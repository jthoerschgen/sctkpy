# -*- coding: utf-8 -*-

"""config.py
Desc: Configurable variables used by the project
"""
import os

FULL_TIME_HOURS = 12  # hours to be considered a full-time student

gpa_map: dict[str | None, int | None] = {
    "A": 4,
    "B": 3,
    "C": 2,
    "D": 1,
    "F": 0,
    "I": None,
    "S": None,
    "U": None,
    "DL": None,
    "Y": None,
    "WD": None,
    "": None,
    None: None,
}  # Map for letter to points, where the letter = key, number of points = value


class StudyHourTier:
    """Object for managing logic related to calculating what study hours a
    member would have."""

    def __init__(
        self,
        bound: float,
        condition: str,
        result_in_house: str,
        desc_in_house: str,
        result_out_house: str,
        desc_out_house: str,
    ):
        self.bound = bound
        self.condition = condition
        self.result_in_house: str = result_in_house
        self.desc_in_house: str = desc_in_house
        self.result_out_house: str = result_out_house
        self.desc_out_house: str = desc_out_house

        assert (
            bound >= 0.00 and bound <= 4.00
        ), "Threshold is for GPA, must be between 0.00-4.00"

        assert self.condition in [
            "<",
            "<=",
            "==",
            "!=",
            ">",
            ">=",
        ], "Invalid condition"

        compare_functions = {
            "<": lambda x, y: x < y,
            "<=": lambda x, y: x <= y,
            "==": lambda x, y: x == y,
            "!=": lambda x, y: x != y,
            ">": lambda x, y: x > y,
            ">=": lambda x, y: x >= y,
        }
        self.compare = compare_functions[self.condition]

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
        ), "Threshold is for GPA, must be between 0.00-4.00"
        return self.compare(x=gpa, y=self.bound)


class StrikeTier(StudyHourTier):
    """Child class of StudyHourTier"""

    def __init__(
        self,
        bound: float,
        condition: str,
        result_in_house: str,
        desc_in_house: str,
        result_out_house: str,
        desc_out_house: str,
        num_chances: int,
    ):
        super().__init__(
            bound,
            condition,
            result_in_house,
            desc_in_house,
            result_out_house,
            desc_out_house,
        )
        self.num_chances: int = num_chances


"""Study Hour GPA Tiers
"""
no_study_hours = StudyHourTier(
    bound=3.00,
    condition=">=",
    result_in_house="",
    desc_in_house="0 Hours Nightly",
    result_out_house="",
    desc_out_house="0 Hours Weekly",
)
tier_one = StudyHourTier(
    bound=3.00,
    condition="<",
    result_in_house="2",
    desc_in_house="2 Hours Nightly (Sun-Thu)",
    result_out_house="5 Weekly",
    desc_out_house="5 Hours Weekly",
)
tier_two = StudyHourTier(
    bound=2.75,
    condition="<",
    result_in_house="4",
    desc_in_house="4 Hours Nightly (Sun-Thu)",
    result_out_house="10 Weekly",
    desc_out_house="10 Hours Weekly",
)
no_punting = StudyHourTier(
    bound=2.60,
    condition="<",
    result_in_house="NP",
    desc_in_house="No Punting",
    result_out_house="",
    desc_out_house="",
)
social_probation = StudyHourTier(
    bound=2.50,
    condition="<",
    result_in_house="SP",
    desc_in_house="Social Probation",
    result_out_house="SP",
    desc_out_house="Social Probation",
)


reduce_two_tiers = StudyHourTier(
    bound=3.50,
    condition=">=",
    result_in_house=no_study_hours.result_in_house,
    desc_in_house=no_study_hours.desc_in_house,
    result_out_house=no_study_hours.result_out_house,
    desc_out_house=no_study_hours.desc_out_house,
)


def get_reduce_one_tier(previous_gpa: float) -> StudyHourTier:
    """Make StudyHourTier object for testing if study hours can be reduced by
    one tier.

    Args:
        previous_gpa (float): GPA from the previous term.

    Returns:
        StudyHourTier: Depending on the given previous GPA, the outcome will
            either be reduced from:
                tier two -> tier one or tier one -> no study hours.
    """
    return StudyHourTier(
        bound=3.00,
        condition=">=",
        result_in_house=(
            tier_one.result_in_house
            if tier_two.test_tier(previous_gpa)
            else no_study_hours.result_in_house
        ),
        desc_in_house=(
            tier_one.desc_in_house
            if tier_two.test_tier(previous_gpa)
            else no_study_hours.desc_in_house
        ),
        result_out_house=(
            tier_one.result_out_house
            if tier_two.test_tier(previous_gpa)
            else no_study_hours.result_out_house
        ),
        desc_out_house=(
            tier_one.desc_out_house
            if tier_two.test_tier(previous_gpa)
            else no_study_hours.desc_out_house
        ),
    )


def get_reduce_two_tiers() -> StudyHourTier:
    """Make StudyHourTier object for testing if study hours can be reduced by
    two tiers.

    Returns:
        StudyHourTier: Depending on the given previous GPA, the outcome will
        either reduce two study hour tiers or not.
    """
    return StudyHourTier(
        bound=3.50,
        condition=">=",
        result_in_house=no_study_hours.result_in_house,
        desc_in_house=no_study_hours.desc_in_house,
        result_out_house=no_study_hours.result_out_house,
        desc_out_house=no_study_hours.desc_out_house,
    )


def get_reduce_no_punting() -> StudyHourTier:
    """Make StudyHourTier object for testing if punting privileges can be
    restored.

    Returns:
        StudyHourTier: Depending on the given previous GPA, the outcome will
        either restore punting privileges or not.
    """
    return StudyHourTier(
        bound=3.00,
        condition=">=",
        result_in_house="",
        desc_in_house="",
        result_out_house="",
        desc_out_house="",
    )


def get_reduce_social_probation() -> StudyHourTier:
    """Make StudyHourTier object for testing if academic social probation can
    be lifted.

    Returns:
        StudyHourTier: Depending on the given previous GPA, the outcome will
        either lift academic social probation or not.
    """
    return StudyHourTier(
        bound=3.25,
        condition=">=",
        result_in_house="",
        desc_in_house="",
        result_out_house="",
        desc_out_house="",
    )


"""Strike GPA Tiers
"""

term_gpa_strike = StrikeTier(
    bound=2.50,
    condition="<",
    result_in_house="",
    desc_in_house="Strike (Term GPA)",
    result_out_house="",
    desc_out_house="Strike (Term GPA)",
    num_chances=3,
)

term_gpa_super_strike = StrikeTier(
    bound=1.75,
    condition="<",
    result_in_house="",
    desc_in_house="Super Strike (Term GPA)",
    result_out_house="",
    desc_out_house="Super Strike (Term GPA)",
    num_chances=2,
)

# cumulative_gpa_strike = StudyHourTier(
#     bound=2.50,
#     condition="<",
#     result_in_house="",
#     desc_in_house="Strike (Cumulative GPA)",
#     result_out_house="",
#     desc_out_house="Strike (Cumulative GPA)",
# )

"""Path variables
"""

proj_root_dir: str = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)
assert os.path.isdir(proj_root_dir), f"{proj_root_dir}, is not a dir"

app_dir: str = os.path.join(proj_root_dir, "sctkpy")
assert os.path.isdir(app_dir), f"{app_dir}, is not a dir"

grade_report_dir: str = os.path.join(proj_root_dir, "gradereports")
if not os.path.exists(grade_report_dir):
    os.mkdir(grade_report_dir)
assert os.path.isdir(grade_report_dir), f"{grade_report_dir}, is not a dir"

template_form_dir: str = os.path.join(app_dir, "templates")
assert os.path.isdir(template_form_dir), f"{template_form_dir}, is not a dir"

logs_dir: str = os.path.join(app_dir, "logs")
if not os.path.exists(logs_dir):
    os.mkdir(logs_dir)
assert os.path.isdir(logs_dir), f"{logs_dir}, is not a dir"

grade_report_template_path: str = os.path.join(
    template_form_dir, "grade_report_template.xlsx"
)

study_checks_template_path: str = os.path.join(
    template_form_dir, "study_checks_template.xlsx"
)

files_hit_list_template_path: str = os.path.join(
    template_form_dir, "files_hit_list_template.xlsx"
)

individual_report_template_path: str = os.path.join(
    template_form_dir, "individual_grade_report_template.xlsx"
)

db_path: str = os.path.join(app_dir, "db", "sctkpy.db")
if not os.path.exists(os.path.dirname(db_path)):
    os.mkdir(os.path.dirname(db_path))
assert os.path.isdir(
    os.path.dirname(db_path)
), f"{os.path.dirname(db_path)}, is not a dir"

default_roster_csv_path: str = os.path.join(
    proj_root_dir, "greeklife_roster_report.csv"
)
