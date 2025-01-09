"""Tests for No Punting Evaluation Methods for a Member Object.

To execute the tests use the following command in the project root directory:
`pytest --verbose`

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    NO PUNTING EVALUATION TESTS:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests Outline:

  -----------------------------------------------------------------------------
    Test #,	    Sem1,   Sem2,           EXPECTED FINAL RESULT
  -----------------------------------------------------------------------------
    Test 1:		2.50,   END             RESULT: True,   (No Punting)
    Test 2:		2.60,   END             RESULT: False,  (Punting)
    Test 3:		3.00,   END             RESULT: False,  (Punting)

    Test 4:		2.50,   3.00    END     RESULT: False,  (Punting)
    Test 5:		2.50,   2.00    END     RESULT: True,   (No Punting)
    Test 6:		2.50,   2.60    END     RESULT: True,   (No Punting)

    Test 7:		2.60,   3.00    END     RESULT: False,  (Punting)
    Test 8:		2.60,   2.00    END     RESULT: True,   (No Punting)
    Test 9:	    2.60,   2.50    END     RESULT: True,   (No Punting)

  -----------------------------------------------------------------------------

    *Tests provide full MC/DC coverage for social probation evaluation.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

from sctkpy.member.course import Grade
from sctkpy.member.member import Member
from tests.utils import generate_example_terms, gpa_presets

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   TEST SET 1  -   Members with no previous term data
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def test_one_no_punting() -> None:
    """Test One - No Punting Evaluation

    Term 1 GPA:     2.50

    Expected Final Result:  True,   (No Punting)
    """
    terms_data: dict[str, list[Grade]] = {"FS2024": gpa_presets["2.50"]}
    result = Member(
        name="John Doe",
        out_of_house=False,
        terms=generate_example_terms(
            input_terms=terms_data, term_cumulative_gpa=3.00
        ),
    ).is_on_no_punting("FS2024")
    assert result is True


def test_two_no_punting() -> None:
    """Test Two - No Punting Evaluation

    Term 1 GPA:     2.60

    Expected Final Result:  False,  (Punting)
    """
    terms_data: dict[str, list[Grade]] = {"FS2024": gpa_presets["2.60"]}
    result = Member(
        name="John Doe",
        out_of_house=False,
        terms=generate_example_terms(
            input_terms=terms_data, term_cumulative_gpa=3.00
        ),
    ).is_on_no_punting("FS2024")
    assert result is False


def test_three_no_punting() -> None:
    """Test Three - No Punting Evaluation

    Term 1 GPA:     3.00

    Expected Final Result:  False,  (Punting)
    """
    terms_data: dict[str, list[Grade]] = {"FS2024": gpa_presets["3.00"]}
    result = Member(
        name="John Doe",
        out_of_house=False,
        terms=generate_example_terms(
            input_terms=terms_data, term_cumulative_gpa=3.00
        ),
    ).is_on_no_punting("FS2024")
    assert result is False


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   TEST SET 2  -   Members with previous term data - previously on no-punting
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def test_four_no_punting() -> None:
    """Test Four - No Punting Evaluation

    Term 1 GPA:     2.50
    Term 2 GPA:     3.00

    Expected Final Result:  False,  (Punting)
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
    ).is_on_no_punting("FS2024")
    assert result is False


def test_five_no_punting() -> None:
    """Test Five - No Punting Evaluation

    Term 1 GPA:     2.50
    Term 2 GPA:     2.00

    Expected Final Result:  True,   (No Punting)
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
    ).is_on_no_punting("FS2024")
    assert result is True


def test_six_no_punting() -> None:
    """Test Six - No Punting Evaluation

    Term 1 GPA:     2.50
    Term 2 GPA:     2.60

    Expected Final Result:  True,   (No Punting)
    """
    terms_data: dict[str, list[Grade]] = {
        "SP2024": gpa_presets["2.50"],
        "FS2024": gpa_presets["2.60"],
    }
    result = Member(
        name="John Doe",
        out_of_house=False,
        terms=generate_example_terms(
            input_terms=terms_data, term_cumulative_gpa=3.00
        ),
    ).is_on_no_punting("FS2024")
    assert result is True


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   TEST SET 3  -   Members with previous term data - not previously no-punting
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def test_seven_no_punting() -> None:
    """Test Seven - No Punting Evaluation

    Term 1 GPA:     2.60
    Term 2 GPA:     3.00

    Expected Final Result:  False,  (Punting)
    """
    terms_data: dict[str, list[Grade]] = {
        "SP2024": gpa_presets["2.60"],
        "FS2024": gpa_presets["3.00"],
    }
    result = Member(
        name="John Doe",
        out_of_house=False,
        terms=generate_example_terms(
            input_terms=terms_data, term_cumulative_gpa=3.00
        ),
    ).is_on_no_punting("FS2024")
    assert result is False


def test_eight_no_punting() -> None:
    """Test Eight - No Punting Evaluation

    Term 1 GPA:     2.60
    Term 2 GPA:     2.00

    Expected Final Result:  True,   (No Punting)
    """
    terms_data: dict[str, list[Grade]] = {
        "SP2024": gpa_presets["2.60"],
        "FS2024": gpa_presets["2.00"],
    }
    result = Member(
        name="John Doe",
        out_of_house=False,
        terms=generate_example_terms(
            input_terms=terms_data, term_cumulative_gpa=3.00
        ),
    ).is_on_no_punting("FS2024")
    assert result is True


def test_nine_no_punting() -> None:
    """Test Eight - No Punting Evaluation

    Term 1 GPA:     2.60
    Term 2 GPA:     2.50

    Expected Final Result:  True,   (No Punting)
    """
    terms_data: dict[str, list[Grade]] = {
        "SP2024": gpa_presets["2.60"],
        "FS2024": gpa_presets["2.50"],
    }
    result = Member(
        name="John Doe",
        out_of_house=False,
        terms=generate_example_terms(
            input_terms=terms_data, term_cumulative_gpa=3.00
        ),
    ).is_on_no_punting("FS2024")
    assert result is True
