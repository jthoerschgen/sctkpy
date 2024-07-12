# -*- coding: utf-8 -*-

import logging

from context import sctkpy

import sctkpy.config
import sctkpy.member

reduce_no_punting = sctkpy.config.reduce_no_punting
reduce_one_tier = sctkpy.config.reduce_one_tier
reduce_social_probation = sctkpy.config.reduce_social_probation
reduce_two_tiers = sctkpy.config.reduce_two_tiers

no_punting = sctkpy.config.no_punting
no_study_hours = sctkpy.config.no_study_hours
social_probation = sctkpy.config.social_probation
tier_one = sctkpy.config.tier_one
tier_two = sctkpy.config.tier_two

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.debug("Testing Member Object")

    # Testing GPA revaluations
    term_null: list[sctkpy.member.Class] = [
        sctkpy.member.Class(
            class_name="", catalog_no="", hrs=3, grade=letter_grade
        )
        for letter_grade in ["I", "I", "I", "I"]
    ]

    term_2_50: list[sctkpy.member.Class] = [
        sctkpy.member.Class(
            class_name="", catalog_no="", hrs=3, grade=letter_grade
        )
        for letter_grade in ["B", "B", "C", "C"]
    ]

    term_2_75: list[sctkpy.member.Class] = [
        sctkpy.member.Class(
            class_name="", catalog_no="", hrs=3, grade=letter_grade
        )
        for letter_grade in ["B", "B", "B", "C"]
    ]

    term_3_00: list[sctkpy.member.Class] = [
        sctkpy.member.Class(
            class_name="", catalog_no="", hrs=3, grade=letter_grade
        )
        for letter_grade in ["B", "B", "B", "B"]
    ]

    term_3_50: list[sctkpy.member.Class] = [
        sctkpy.member.Class(
            class_name="", catalog_no="", hrs=3, grade=letter_grade
        )
        for letter_grade in ["A", "A", "B", "B"]
    ]

    test_terms = [
        sctkpy.member.Term(
            term=("FS" if (i % 2 == 0) else "SP") + str(2020 + (i + 1 // 2)),
            chapter="Beta Sigma Psi",
            new_member=True if i == 0 else False,
            priv_gpa=0.00,
            priv_cum_gpa=0.00,
            term_gpa=0.00,
            term_cum_gpa=0.00,
            classes=test_classes,
        )
        for i, test_classes in enumerate(
            [
                term_3_50,  # 1
                term_2_50,  # 2
                term_2_75,  # 3
                term_2_75,  # 4
                term_3_50,  # 5
                term_2_75,  # 6
                term_3_00,  # 7
                term_2_50,  # 8
                term_3_00,  # 9
                term_null,  # 10
                term_2_50,  # 11
                term_3_00,  # 12
                term_2_75,  # 13
                term_3_00,  # 14
                term_2_75,  # 15
                term_2_75,  # 16
                term_2_50,  # 17
                term_2_50,  # 18
                term_3_00,  # 19
                term_2_75,  # 20
            ]
        )
    ]

    expected_results = [
        no_study_hours.result_in_house,  # 1
        tier_two.result_in_house + " " + no_punting.result_in_house,  # 2
        tier_two.result_in_house + " " + no_punting.result_in_house,  # 3
        tier_two.result_in_house + " " + no_punting.result_in_house,  # 4
        no_study_hours.result_in_house,  # 5
        tier_one.result_in_house,  # 6
        no_study_hours.result_in_house,  # 7
        tier_two.result_in_house + " " + no_punting.result_in_house,  # 8
        tier_one.result_in_house,  # 9
        tier_one.result_in_house,  # 10
        tier_two.result_in_house + " " + no_punting.result_in_house,  # 11
        tier_one.result_in_house,  # 12
        tier_one.result_in_house,  # 13
        no_study_hours.result_in_house,  # 14
        tier_one.result_in_house,  # 15
        tier_one.result_in_house,  # 16
        tier_two.result_in_house + " " + no_punting.result_in_house,  # 17
        tier_two.result_in_house + " " + no_punting.result_in_house,  # 18
        tier_one.result_in_house,  # 19
        tier_one.result_in_house,  # 20
    ]
    # expected_results = [
    #     no_study_hours.result_in_house,  # 1
    #     tier_two.result_in_house,  # 2
    #     tier_two.result_in_house,  # 3
    #     tier_two.result_in_house,  # 4
    #     no_study_hours.result_in_house,  # 5
    #     tier_one.result_in_house,  # 6
    #     no_study_hours.result_in_house,  # 7
    #     tier_two.result_in_house,  # 8
    #     tier_one.result_in_house,  # 9
    #     tier_one.result_in_house,  # 10
    #     tier_two.result_in_house,  # 11
    #     tier_one.result_in_house,  # 12
    #     tier_one.result_in_house,  # 13
    #     no_study_hours.result_in_house,  # 14
    #     tier_one.result_in_house,  # 15
    #     tier_one.result_in_house,  # 16
    #     tier_two.result_in_house,  # 17
    #     tier_two.result_in_house,  # 18
    #     tier_one.result_in_house,  # 19
    #     tier_one.result_in_house,  # 20
    # ]

    test_member = sctkpy.member.Member(
        name="First Last",
        out_of_house=False,
        terms={test_term.term: test_term for test_term in test_terms},
    )

    for i, term in enumerate(test_member.terms):
        (_, gpa), (previous_term, previous_gpa), result = (
            test_member.study_hours(term)
        )
        print(f"#{i + 1}\tTerm: {term},\tGPA: {gpa},\tResult: {result}")
        assert (
            result == expected_results[i]
        ), f"#{i + 1}\t{result} != {expected_results[i]}"
