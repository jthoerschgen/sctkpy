"""Configuration for the project."""

import os
import tomllib

from sctkpy.member.study_hour_tier import (
    StrikeTier,
    StudyHourTier,
    StudyHourTierCumulative,
)

proj_root_dir: str = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)
assert os.path.isdir(proj_root_dir), f"{proj_root_dir}, is not a dir"

app_dir: str = os.path.join(proj_root_dir, "sctkpy")
assert os.path.isdir(app_dir), f"{app_dir}, is not a dir"

template_form_dir: str = os.path.join(app_dir, "templates")
assert os.path.isdir(template_form_dir), f"{template_form_dir}, is not a dir"

grade_report_template_path: str = os.path.join(
    template_form_dir, "grade_report_template.xlsx"
)

study_checks_template_path: str = os.path.join(
    template_form_dir, "study_checks_template.xlsx"
)

files_hit_list_template_path: str = os.path.join(
    template_form_dir, "files_hit_list_template.xlsx"
)

member_report_template_path: str = os.path.join(
    template_form_dir, "member_report_template.xlsx"
)

logs_dir: str = os.path.join(app_dir, "logs")
if not os.path.exists(logs_dir):
    os.mkdir(logs_dir)
assert os.path.isdir(logs_dir), f"{logs_dir}, is not a dir"

with open(os.path.join(app_dir, "config.toml"), mode="rb") as config_toml_file:
    config = tomllib.load(config_toml_file)

    no_study_hours = StudyHourTier(
        bound=config["tier"]["no_study_hours"]["bound"],
        condition=config["tier"]["no_study_hours"]["condition"],
        result_in_house=config["tier"]["no_study_hours"]["result_in_house"],
        description_in_house=config["tier"]["no_study_hours"][
            "description_in_house"
        ],
        result_out_house=config["tier"]["no_study_hours"]["result_out_house"],
        description_out_house=config["tier"]["no_study_hours"][
            "description_out_house"
        ],
    )
    tier_one = StudyHourTier(
        bound=config["tier"]["tier_one"]["bound"],
        condition=config["tier"]["tier_one"]["condition"],
        result_in_house=config["tier"]["tier_one"]["result_in_house"],
        description_in_house=config["tier"]["tier_one"][
            "description_in_house"
        ],
        result_out_house=config["tier"]["tier_one"]["result_out_house"],
        description_out_house=config["tier"]["tier_one"][
            "description_out_house"
        ],
    )
    tier_two = StudyHourTier(
        bound=config["tier"]["tier_two"]["bound"],
        condition=config["tier"]["tier_two"]["condition"],
        result_in_house=config["tier"]["tier_two"]["result_in_house"],
        description_in_house=config["tier"]["tier_two"][
            "description_in_house"
        ],
        result_out_house=config["tier"]["tier_two"]["result_out_house"],
        description_out_house=config["tier"]["tier_two"][
            "description_out_house"
        ],
    )
    no_punting = StudyHourTier(
        bound=config["tier"]["no_punting"]["bound"],
        condition=config["tier"]["no_punting"]["condition"],
        result_in_house=config["tier"]["no_punting"]["result_in_house"],
        description_in_house=config["tier"]["no_punting"][
            "description_in_house"
        ],
        result_out_house=config["tier"]["no_punting"]["result_out_house"],
        description_out_house=config["tier"]["no_punting"][
            "description_out_house"
        ],
    )
    social_probation = StudyHourTier(
        bound=config["tier"]["social_probation"]["bound"],
        condition=config["tier"]["social_probation"]["condition"],
        result_in_house=config["tier"]["social_probation"]["result_in_house"],
        description_in_house=config["tier"]["social_probation"][
            "description_in_house"
        ],
        result_out_house=config["tier"]["social_probation"][
            "result_out_house"
        ],
        description_out_house=config["tier"]["social_probation"][
            "description_out_house"
        ],
    )

    reduce_two_tiers = StudyHourTierCumulative(
        term_bound=config["tier"]["reduce_two_tiers"]["term_bound"],
        term_condition=config["tier"]["reduce_two_tiers"]["term_condition"],
        cumulative_bound=config["tier"]["reduce_two_tiers"][
            "cumulative_bound"
        ],
        cumulative_condition=config["tier"]["reduce_two_tiers"][
            "cumulative_condition"
        ],
        description_in_house=config["tier"]["reduce_two_tiers"][
            "description_in_house"
        ],
        description_out_house=config["tier"]["reduce_two_tiers"][
            "description_out_house"
        ],
    )
    reduce_one_tier = StudyHourTierCumulative(
        term_bound=config["tier"]["reduce_one_tier"]["term_bound"],
        term_condition=config["tier"]["reduce_one_tier"]["term_condition"],
        cumulative_bound=config["tier"]["reduce_one_tier"]["cumulative_bound"],
        cumulative_condition=config["tier"]["reduce_one_tier"][
            "cumulative_condition"
        ],
        description_in_house=config["tier"]["reduce_one_tier"][
            "description_in_house"
        ],
        description_out_house=config["tier"]["reduce_one_tier"][
            "description_out_house"
        ],
    )
    get_off_no_punting = StudyHourTier(
        bound=config["tier"]["get_off_no_punting"]["bound"],
        condition=config["tier"]["get_off_no_punting"]["condition"],
        result_in_house=config["tier"]["get_off_no_punting"][
            "result_in_house"
        ],
        description_in_house=config["tier"]["get_off_no_punting"][
            "description_in_house"
        ],
        result_out_house=config["tier"]["get_off_no_punting"][
            "result_out_house"
        ],
        description_out_house=config["tier"]["get_off_no_punting"][
            "description_out_house"
        ],
    )
    get_off_social_probation = StudyHourTier(
        bound=config["tier"]["get_off_social_probation"]["bound"],
        condition=config["tier"]["get_off_social_probation"]["condition"],
        result_in_house=config["tier"]["get_off_social_probation"][
            "result_in_house"
        ],
        description_in_house=config["tier"]["get_off_social_probation"][
            "description_in_house"
        ],
        result_out_house=config["tier"]["get_off_social_probation"][
            "result_out_house"
        ],
        description_out_house=config["tier"]["get_off_social_probation"][
            "description_out_house"
        ],
    )

    academic_suspension_term = StudyHourTier(
        bound=config["tier"]["academic_suspension_term"]["bound"],
        condition=config["tier"]["academic_suspension_term"]["condition"],
        result_in_house=config["tier"]["academic_suspension_term"][
            "result_in_house"
        ],
        description_in_house=config["tier"]["academic_suspension_term"][
            "description_in_house"
        ],
        result_out_house=config["tier"]["academic_suspension_term"][
            "result_out_house"
        ],
        description_out_house=config["tier"]["academic_suspension_term"][
            "description_out_house"
        ],
    )
    academic_suspension_cumulative = StudyHourTier(
        bound=config["tier"]["academic_suspension_cumulative"]["bound"],
        condition=config["tier"]["academic_suspension_cumulative"][
            "condition"
        ],
        result_in_house=config["tier"]["academic_suspension_cumulative"][
            "result_in_house"
        ],
        description_in_house=config["tier"]["academic_suspension_cumulative"][
            "description_in_house"
        ],
        result_out_house=config["tier"]["academic_suspension_cumulative"][
            "result_out_house"
        ],
        description_out_house=config["tier"]["academic_suspension_cumulative"][
            "description_out_house"
        ],
    )
    strike = StrikeTier(
        bound=config["tier"]["strike"]["bound"],
        condition=config["tier"]["strike"]["condition"],
        number_chances=config["tier"]["strike"]["number_chances"],
        result_in_house=config["tier"]["strike"]["result_in_house"],
        description_in_house=config["tier"]["strike"]["description_in_house"],
        result_out_house=config["tier"]["strike"]["result_out_house"],
        description_out_house=config["tier"]["strike"][
            "description_out_house"
        ],
    )
    super_strike = StrikeTier(
        bound=config["tier"]["super_strike"]["bound"],
        condition=config["tier"]["super_strike"]["condition"],
        number_chances=config["tier"]["super_strike"]["number_chances"],
        result_in_house=config["tier"]["super_strike"]["result_in_house"],
        description_in_house=config["tier"]["super_strike"][
            "description_in_house"
        ],
        result_out_house=config["tier"]["super_strike"]["result_out_house"],
        description_out_house=config["tier"]["super_strike"][
            "description_out_house"
        ],
    )
