"""Tests for Social Probation Evaluation Methods for a Member Object.

To execute the tests use the following command in the project root directory:
`pytest --verbose`

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    SOCIAL PROBATION EVALUATION TESTS:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests Outline:

  -----------------------------------------------------------------------------
    Test #,	    Sem1,   Sem2,           EXPECTED FINAL RESULT
  -----------------------------------------------------------------------------
    Test 1:		2.00,   END             RESULT: True,   (Social Probation)
    Test 2:		2.50,   END             RESULT: False,  (No Social Probation)
    Test 3:		3.00,   END             RESULT: False,  (No Social Probation)

    Test 4:		2.00,   3.25    END     RESULT: False,  (No Social Probation)
    Test 5:		2.00,   2.00    END     RESULT: True,   (Social Probation)
    Test 6:		2.00,   2.50    END     RESULT: True,   (Social Probation)
    Test 7:		2.00,   3.00    END     RESULT: True,   (Social Probation)

    Test 8:		2.50,   3.25    END     RESULT: False,  (No Social Probation)
    Test 9:		2.50,   2.00    END     RESULT: True,   (Social Probation)
    Test 10:	2.50,   2.50    END     RESULT: False,  (No Social Probation)
    Test 11:	2.50,   3.00    END     RESULT: False,  (No Social Probation)

  -----------------------------------------------------------------------------

    *Tests provide full MC/DC coverage for social probation evaluation.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

from sctkpy.member.course import Grade
from sctkpy.member.member import Member
from tests.utils import generate_example_terms, gpa_presets

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   TEST SET 1  -   Members with no previous term data
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def test_one_social_probation() -> None:
    """Test One - Social Probation Evaluation

    Term 1 GPA:     2.00

    Expected Final Result:  True,   (Social Probation)
    """
    terms_data: dict[str, list[Grade]] = {"FS2024": gpa_presets["2.00"]}
    result = Member(
        name="John Doe",
        out_of_house=False,
        terms=generate_example_terms(
            input_terms=terms_data, term_cumulative_gpa=3.00
        ),
    ).is_on_social_probation("FS2024")
    assert result is True


def test_two_social_probation() -> None:
    """Test Two - Social Probation Evaluation

    Term 1 GPA:     2.50

    Expected Final Result:  False,  (No Social Probation)
    """
    terms_data: dict[str, list[Grade]] = {"FS2024": gpa_presets["2.50"]}
    result = Member(
        name="John Doe",
        out_of_house=False,
        terms=generate_example_terms(
            input_terms=terms_data, term_cumulative_gpa=3.00
        ),
    ).is_on_social_probation("FS2024")
    assert result is False


def test_three_social_probation() -> None:
    """Test Three - Social Probation Evaluation

    Term 1 GPA:     3.00

    Expected Final Result:  False,  (No Social Probation)
    """
    terms_data: dict[str, list[Grade]] = {"FS2024": gpa_presets["3.00"]}
    result = Member(
        name="John Doe",
        out_of_house=False,
        terms=generate_example_terms(
            input_terms=terms_data, term_cumulative_gpa=3.00
        ),
    ).is_on_social_probation("FS2024")
    assert result is False


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   TEST SET 2  -   Members with previous term data - previously on so-pro
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def test_four_social_probation() -> None:
    """Test Four - Social Probation Evaluation

    Term 1 GPA:     2.00
    Term 2 GPA:     3.25

    Expected Final Result:  False,  (No Social Probation)
    """
    terms_data: dict[str, list[Grade]] = {
        "SP2024": gpa_presets["2.00"],
        "FS2024": gpa_presets["3.25"],
    }
    result = Member(
        name="John Doe",
        out_of_house=False,
        terms=generate_example_terms(
            input_terms=terms_data, term_cumulative_gpa=3.00
        ),
    ).is_on_social_probation("FS2024")
    assert result is False


def test_five_social_probation() -> None:
    """Test Five - Social Probation Evaluation

    Term 1 GPA:     2.00
    Term 2 GPA:     2.00

    Expected Final Result:  True,   (Social Probation)
    """
    terms_data: dict[str, list[Grade]] = {
        "SP2024": gpa_presets["2.00"],
        "FS2024": gpa_presets["2.00"],
    }
    result = Member(
        name="John Doe",
        out_of_house=False,
        terms=generate_example_terms(
            input_terms=terms_data, term_cumulative_gpa=3.00
        ),
    ).is_on_social_probation("FS2024")
    assert result is True


def test_six_social_probation() -> None:
    """Test Six - Social Probation Evaluation

    Term 1 GPA:     2.00
    Term 2 GPA:     2.50

    Expected Final Result:  True,   (Social Probation)
    """
    terms_data: dict[str, list[Grade]] = {
        "SP2024": gpa_presets["2.00"],
        "FS2024": gpa_presets["2.50"],
    }
    result = Member(
        name="John Doe",
        out_of_house=False,
        terms=generate_example_terms(
            input_terms=terms_data, term_cumulative_gpa=3.00
        ),
    ).is_on_social_probation("FS2024")
    assert result is True


def test_seven_social_probation() -> None:
    """Test Seven - Social Probation Evaluation

    Term 1 GPA:     2.00
    Term 2 GPA:     3.00

    Expected Final Result:  True,   (Social Probation)
    """
    terms_data: dict[str, list[Grade]] = {
        "SP2024": gpa_presets["2.00"],
        "FS2024": gpa_presets["3.00"],
    }
    result = Member(
        name="John Doe",
        out_of_house=False,
        terms=generate_example_terms(
            input_terms=terms_data, term_cumulative_gpa=3.00
        ),
    ).is_on_social_probation("FS2024")
    assert result is True


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   TEST SET 3  -   Members with previous term data - not previously on so-pro
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def test_eight_social_probation() -> None:
    """Test Eight - Social Probation Evaluation

    Term 1 GPA:     2.50
    Term 2 GPA:     3.25

    Expected Final Result:  False,  (No Social Probation)
    """
    terms_data: dict[str, list[Grade]] = {
        "SP2024": gpa_presets["2.50"],
        "FS2024": gpa_presets["3.25"],
    }
    result = Member(
        name="John Doe",
        out_of_house=False,
        terms=generate_example_terms(
            input_terms=terms_data, term_cumulative_gpa=3.00
        ),
    ).is_on_social_probation("FS2024")
    assert result is False


def test_nine_social_probation() -> None:
    """Test Nine - Social Probation Evaluation

    Term 1 GPA:     2.50
    Term 2 GPA:     2.00

    Expected Final Result:  True,   (Social Probation)
    """
    terms_data: dict[str, list[Grade]] = {
        "SP2024": gpa_presets["2.50"],
        "FS2024": gpa_presets["2.00"],
    }
    result = Member(
        name="John Doe",
        out_of_house=False,
        terms=generate_example_terms(
            input_terms=terms_data, term_cumulative_gpa=3.00
        ),
    ).is_on_social_probation("FS2024")
    assert result is True


def test_ten_social_probation() -> None:
    """Test Ten - Social Probation Evaluation

    Term 1 GPA:     2.50
    Term 2 GPA:     2.50

    Expected Final Result:  False,  (No Social Probation)
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
    ).is_on_social_probation("FS2024")
    assert result is False


def test_eleven_social_probation() -> None:
    """Test Eleven - Social Probation Evaluation

    Term 1 GPA:     2.50
    Term 2 GPA:     3.00

    Expected Final Result:  False,  (No Social Probation)
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
    ).is_on_social_probation("FS2024")
    assert result is False
