"""Tests for Study Hour Evaluation Methods for a Member Object.

To execute the tests use the following command in the project root directory:
`pytest --verbose`

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   STUDY HOUR EVALUATION TESTS:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   Tests Outline:

  -----------------------------------------------------------------------------
    Test #,	    Cum. GPA,   Sem1,   Sem2,           EXPECTED FINAL RESULT
  -----------------------------------------------------------------------------
    Test 1:		3.00	    2.50,   END             RESULT: 4 Study Hours
    Test 2:     3.00	    2.75,   END             RESULT: 2 Study Hours
    Test 3:     3.00	    3.00,   END             RESULT: 0 Study Hours

    Test 4a:    3.00	    2.50,   3.50,   END     RESULT: 0 Study Hours
    Test 4b:    2.74	    2.50,   3.50,   END     RESULT: 4 Study Hours
    Test 5a:    3.00	    2.50,   3.00,   END     RESULT: 2 Study Hours
    Test 5b:    2.74	    2.50,   3.00,   END     RESULT: 4 Study Hours
    Test 6a:    3.00	    2.50,   2.75,   END     RESULT: 4 Study Hours
    Test 6b:    3.00	    2.50,   2.50,   END     RESULT: 4 Study Hours

    Test 7a:    3.00	    2.75,   3.00,   END     RESULT: 0 Study Hours
    Test 7b:    2.74	    2.75,   3.00,   END     RESULT: 2 Study Hours
    Test 7c:    2.74	    2.75,   3.50,   END     RESULT: 2 Study Hours
    Test 8:     3.00	    2.75,   2.50,   END     RESULT: 4 Study Hours
    Test 9:     3.00	    2.75,   2.75,   END     RESULT: 2 Study Hours

    Test 10:    3.00	    3.00,   2.50,   END     RESULT: 4 Study Hours
    Test 11:    3.00	    3.00,   2.75,   END     RESULT: 2 Study Hours
    Test 12:    3.00	    3.00,   3.00,   END     RESULT: 0 Study Hours
  -----------------------------------------------------------------------------

    *Tests provide full MC/DC coverage for study hour evaluation.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

from sctkpy.config import no_study_hours, tier_one, tier_two
from sctkpy.member.course import Grade
from sctkpy.member.member import Member
from tests.utils import generate_example_terms, gpa_presets

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   TEST SET 1  -   Members with no previous term data
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def test_one_study_hour_evaluation() -> None:
    """Test One - Study Hour Evaluation

    Cumulative GPA: 3.00

    Term 1 GPA:     2.50

    Expected Final Result:  4 Study Hours
    """
    terms_data: dict[str, list[Grade]] = {"FS2024": gpa_presets["2.50"]}
    result = Member(
        name="John Doe",
        out_of_house=False,
        terms=generate_example_terms(
            input_terms=terms_data, term_cumulative_gpa=3.00
        ),
    ).determine_study_hours("FS2024", on_social_probation=False)
    assert result == tier_two


def test_two_study_hour_evaluation() -> None:
    """Test Two - Study Hour Evaluation

    Cumulative GPA: 3.00

    Term 1 GPA:     2.75

    Expected Final Result:  2 Study Hours
    """
    terms_data: dict[str, list[Grade]] = {"FS2024": gpa_presets["2.75"]}
    result = Member(
        name="John Doe",
        out_of_house=False,
        terms=generate_example_terms(
            input_terms=terms_data, term_cumulative_gpa=3.00
        ),
    ).determine_study_hours("FS2024", on_social_probation=False)
    assert result == tier_one


def test_three_study_hour_evaluation() -> None:
    """Test Three - Study Hour Evaluation

    Cumulative GPA: 3.00

    Term 1 GPA:     3.00

    Expected Final Result:  No Study Hours
    """
    terms_data: dict[str, list[Grade]] = {"FS2024": gpa_presets["3.00"]}
    result = Member(
        name="John Doe",
        out_of_house=False,
        terms=generate_example_terms(
            input_terms=terms_data, term_cumulative_gpa=3.00
        ),
    ).determine_study_hours("FS2024", on_social_probation=False)
    assert result == no_study_hours


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   TEST SET 2  -   Members with 4 study hours previously
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def test_four_a_study_hour_evaluation() -> None:
    """Test Four A - Study Hour Evaluation

    Cumulative GPA: 3.00

    Term 1 GPA:     2.50
    Term 2 GPA:     3.50

    Expected Final Result:  No Study Hours
    """
    terms_data: dict[str, list[Grade]] = {
        "SP2024": gpa_presets["2.50"],
        "FS2024": gpa_presets["3.50"],
    }
    result = Member(
        name="John Doe",
        out_of_house=False,
        terms=generate_example_terms(
            input_terms=terms_data, term_cumulative_gpa=3.00
        ),
    ).determine_study_hours("FS2024", on_social_probation=False)
    assert result == no_study_hours


def test_four_b_study_hour_evaluation() -> None:
    """Test Four B - Study Hour Evaluation

    Cumulative GPA: 2.74

    Term 1 GPA:     2.50
    Term 2 GPA:     3.50

    Expected Final Result:  4 Study Hours
    """
    terms_data: dict[str, list[Grade]] = {
        "SP2024": gpa_presets["2.50"],
        "FS2024": gpa_presets["3.50"],
    }
    result = Member(
        name="John Doe",
        out_of_house=False,
        terms=generate_example_terms(
            input_terms=terms_data, term_cumulative_gpa=2.74
        ),
    ).determine_study_hours("FS2024", on_social_probation=False)
    assert result == tier_two


def test_five_a_study_hour_evaluation() -> None:
    """Test Five A - Study Hour Evaluation

    Cumulative GPA: 3.00

    Term 1 GPA:     2.50
    Term 2 GPA:     3.00

    Expected Final Result:  2 Study Hours
    """
    terms_data: dict[str, list[Grade]] = {
        "SP2024": gpa_presets["2.50"],
        "FS2024": gpa_presets["3.00"],
    }
    result = Member(
        name="John Doe",
        out_of_house=False,
        terms=generate_example_terms(
            input_terms=terms_data, term_cumulative_gpa=3.00
        ),
    ).determine_study_hours("FS2024", on_social_probation=False)
    assert result == tier_one


def test_five_b_study_hour_evaluation() -> None:
    """Test Five B - Study Hour Evaluation

    Cumulative GPA: 2.74

    Term 1 GPA:     2.50
    Term 2 GPA:     3.00

    Expected Final Result:  4 Study Hours
    """
    terms_data: dict[str, list[Grade]] = {
        "SP2024": gpa_presets["2.50"],
        "FS2024": gpa_presets["3.00"],
    }
    result = Member(
        name="John Doe",
        out_of_house=False,
        terms=generate_example_terms(
            input_terms=terms_data, term_cumulative_gpa=2.74
        ),
    ).determine_study_hours("FS2024", on_social_probation=False)
    assert result == tier_two


def test_six_a_study_hour_evaluation() -> None:
    """Test Six A - Study Hour Evaluation

    Cumulative GPA: 3.00

    Term 1 GPA:     2.50
    Term 2 GPA:     2.75

    Expected Final Result:  4 Study Hours
    """
    terms_data: dict[str, list[Grade]] = {
        "SP2024": gpa_presets["2.50"],
        "FS2024": gpa_presets["2.75"],
    }
    result = Member(
        name="John Doe",
        out_of_house=False,
        terms=generate_example_terms(
            input_terms=terms_data, term_cumulative_gpa=3.00
        ),
    ).determine_study_hours("FS2024", on_social_probation=False)
    assert result == tier_two


def test_six_b_study_hour_evaluation() -> None:
    """Test Six B - Study Hour Evaluation

    Cumulative GPA: 3.00

    Term 1 GPA:     2.50
    Term 2 GPA:     2.50

    Expected Final Result:  4 Study Hours
    """
    terms_data: dict[str, list[Grade]] = {
        "SP2024": gpa_presets["2.50"],
        "FS2024": gpa_presets["2.50"],
    }
    result = Member(
        name="John Doe",
        out_of_house=False,
        terms=generate_example_terms(
            input_terms=terms_data, term_cumulative_gpa=3.00
        ),
    ).determine_study_hours("FS2024", on_social_probation=False)
    assert result == tier_two


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   TEST SET 3  -   Members with 2 study hours previously
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def test_seven_a_study_hour_evaluation() -> None:
    """Test Seven A - Study Hour Evaluation

    Cumulative GPA: 3.00

    Term 1 GPA:     2.75
    Term 2 GPA:     3.00

    Expected Final Result:  No Study Hours
    """
    terms_data: dict[str, list[Grade]] = {
        "SP2024": gpa_presets["2.75"],
        "FS2024": gpa_presets["3.00"],
    }
    result = Member(
        name="John Doe",
        out_of_house=False,
        terms=generate_example_terms(
            input_terms=terms_data, term_cumulative_gpa=3.00
        ),
    ).determine_study_hours("FS2024", on_social_probation=False)
    assert result == no_study_hours


def test_seven_b_study_hour_evaluation() -> None:
    """Test Seven B - Study Hour Evaluation

    Cumulative GPA: 2.74

    Term 1 GPA:     2.75
    Term 2 GPA:     3.00

    Expected Final Result:  2 Study Hours
    """
    terms_data: dict[str, list[Grade]] = {
        "SP2024": gpa_presets["2.75"],
        "FS2024": gpa_presets["3.00"],
    }
    result = Member(
        name="John Doe",
        out_of_house=False,
        terms=generate_example_terms(
            input_terms=terms_data, term_cumulative_gpa=2.74
        ),
    ).determine_study_hours("FS2024", on_social_probation=False)
    assert result == tier_one


def test_seven_c_study_hour_evaluation() -> None:
    """Test Seven C - Study Hour Evaluation

    Cumulative GPA: 2.74

    Term 1 GPA:     2.75
    Term 2 GPA:     3.50

    Expected Final Result:  2 Study Hours
    """
    terms_data: dict[str, list[Grade]] = {
        "SP2024": gpa_presets["2.75"],
        "FS2024": gpa_presets["3.50"],
    }
    result = Member(
        name="John Doe",
        out_of_house=False,
        terms=generate_example_terms(
            input_terms=terms_data, term_cumulative_gpa=2.74
        ),
    ).determine_study_hours("FS2024", on_social_probation=False)
    assert result == tier_one


def test_eight_study_hour_evaluation() -> None:
    """Test Eight - Study Hour Evaluation

    Cumulative GPA: 3.00

    Term 1 GPA:     2.75
    Term 2 GPA:     2.50

    Expected Final Result:  4 Study Hours
    """
    terms_data: dict[str, list[Grade]] = {
        "SP2024": gpa_presets["2.75"],
        "FS2024": gpa_presets["2.50"],
    }
    result = Member(
        name="John Doe",
        out_of_house=False,
        terms=generate_example_terms(
            input_terms=terms_data, term_cumulative_gpa=3.00
        ),
    ).determine_study_hours("FS2024", on_social_probation=False)
    assert result == tier_two


def test_nine_study_hour_evaluation() -> None:
    """Test Nine - Study Hour Evaluation

    Cumulative GPA: 3.00

    Term 1 GPA:     2.75
    Term 2 GPA:     2.75

    Expected Final Result:  2 Study Hours
    """
    terms_data: dict[str, list[Grade]] = {
        "SP2024": gpa_presets["2.75"],
        "FS2024": gpa_presets["2.75"],
    }
    result = Member(
        name="John Doe",
        out_of_house=False,
        terms=generate_example_terms(
            input_terms=terms_data, term_cumulative_gpa=3.00
        ),
    ).determine_study_hours("FS2024", on_social_probation=False)
    assert result == tier_one


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   TEST SET 4  -   Members with no study hours previously
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def test_ten_study_hour_evaluation() -> None:
    """Test Ten - Study Hour Evaluation

    Cumulative GPA: 3.00

    Term 1 GPA:     3.00
    Term 2 GPA:     2.50

    Expected Final Result:  4 Study Hours
    """
    terms_data: dict[str, list[Grade]] = {
        "SP2024": gpa_presets["3.00"],
        "FS2024": gpa_presets["2.50"],
    }
    result = Member(
        name="John Doe",
        out_of_house=False,
        terms=generate_example_terms(
            input_terms=terms_data, term_cumulative_gpa=3.00
        ),
    ).determine_study_hours("FS2024", on_social_probation=False)
    assert result == tier_two


def test_eleven_study_hour_evaluation() -> None:
    """Test Eleven - Study Hour Evaluation

    Cumulative GPA: 3.00

    Term 1 GPA:     3.00
    Term 2 GPA:     2.75

    Expected Final Result:  2 Study Hours
    """
    terms_data: dict[str, list[Grade]] = {
        "SP2024": gpa_presets["3.00"],
        "FS2024": gpa_presets["2.75"],
    }
    result = Member(
        name="John Doe",
        out_of_house=False,
        terms=generate_example_terms(
            input_terms=terms_data, term_cumulative_gpa=3.00
        ),
    ).determine_study_hours("FS2024", on_social_probation=False)
    assert result == tier_one


def test_twelve_study_hour_evaluation() -> None:
    """Test Twelve - Study Hour Evaluation

    Cumulative GPA: 3.00

    Term 1 GPA:     3.00
    Term 2 GPA:     3.00

    Expected Final Result:  No Study Hours
    """
    terms_data: dict[str, list[Grade]] = {
        "SP2024": gpa_presets["3.00"],
        "FS2024": gpa_presets["3.00"],
    }
    result = Member(
        name="John Doe",
        out_of_house=False,
        terms=generate_example_terms(
            input_terms=terms_data, term_cumulative_gpa=3.00
        ),
    ).determine_study_hours("FS2024", on_social_probation=False)
    assert result == no_study_hours
