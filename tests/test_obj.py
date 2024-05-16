# -*- coding: utf-8 -*-

import logging

from context import sctkpy

import sctkpy.member

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.debug("Testing Member Object")
    # generate example courses
    classes = []
    for grade in sctkpy.config.gpa_map.keys():
        classes.append(
            sctkpy.member.Class(f"{grade} Class", f"100{grade}", 3, grade)
        )

    test_terms = [
        sctkpy.member.Term(
            term="FS2021",
            chapter="Beta Sigma Psi",
            new_member=True,
            priv_gpa=0.00,
            priv_cum_gpa=0.00,
            term_gpa=0.00,
            term_cum_gpa=0.00,
            classes=[
                sctkpy.member.Class(
                    f"{sctkpy.config.gpa_map['A']} Class",
                    f"100{sctkpy.config.gpa_map['A']}",
                    3,
                    "A",
                )
            ]
            * 5,
        ),  # New member with 4.00 GPA
        sctkpy.member.Term(
            term="SP2022",
            chapter="Beta Sigma Psi",
            new_member=False,
            priv_gpa=0.00,
            priv_cum_gpa=0.00,
            term_gpa=0.00,
            term_cum_gpa=0.00,
            classes=classes,
        ),  # Test all potential grades, all but A,B,C,D,F shouldn't affect GPA
    ]

    for term, grades in [
        ("FS2023", ["B", "B", "B", "B", "B"]),  # 3.00 GPA
        ("SP2024", ["A", "A", "A", "D", "D"]),  # 2.80 GPA
        ("FS2024", ["A", "A", "B", "D", "D"]),  # 2.60 GPA
        ("SP2025", ["A", "A", "C", "C", "C", "D"]),  # 2.50 GPA
        ("FS2025", ["A", "A", "A", "F", "F"]),  # 2.40 GPA
    ]:
        test_terms.append(
            sctkpy.member.Term(
                term=term,
                chapter="Beta Sigma Psi",
                new_member=False,
                priv_gpa=0.00,
                priv_cum_gpa=0.00,
                term_gpa=0.00,
                term_cum_gpa=0.00,
                classes=[
                    sctkpy.member.Class(
                        f"{sctkpy.config.gpa_map[grade]} Class",
                        f"100{sctkpy.config.gpa_map[grade]}",
                        3,
                        grade,
                    )
                    for grade in grades
                ],
            ),
        )

    test_member = sctkpy.member.Member(
        name="First Last",
        out_of_house=False,
        terms={test_term.term: test_term for test_term in test_terms},
    )

    logger.debug("Name:         %s", test_member.name)
    logger.debug("Out of House: %s", test_member.out_of_house)
    logger.debug("Terms:        %s", test_member.terms.keys())
    for term in test_member.terms.keys():
        logger.debug("\tTerm: %s", term)
        for course in test_member.terms[term].classes:
            logger.debug("\t\tClass: %s", course.__dict__)

    for term in test_terms:
        ret_term, gpa, study_hour_status = test_member.study_hours(term.term)
        logger.debug("GPA: %f, Status: %s", gpa, study_hour_status)
