"""Test that validates that the GPA presets are correct."""

from tests.utils import generate_example_term, gpa_presets


def test_gpa_calculation_sanity_check() -> None:
    """Sanity check to ensure the GPA presets result in the desired GPA."""
    assert generate_example_term(gpa_presets["2.00"]).calculate_gpa() == 2.00
    assert generate_example_term(gpa_presets["2.50"]).calculate_gpa() == 2.50
    assert generate_example_term(gpa_presets["2.60"]).calculate_gpa() == 2.60
    assert generate_example_term(gpa_presets["2.75"]).calculate_gpa() == 2.75
    assert generate_example_term(gpa_presets["3.00"]).calculate_gpa() == 3.00
    assert generate_example_term(gpa_presets["3.25"]).calculate_gpa() == 3.25
    assert generate_example_term(gpa_presets["3.50"]).calculate_gpa() == 3.50
