from tests.utils import format_results

def test_diabetes_sugar():
    # mock result (engine would return this later)
    mock_result = {
        "warnings": ["Sugar may increase blood glucose for Diabetes"],
        "alternatives": ["Replace sugar with Stevia"]
    }

    format_results(mock_result, case_name="Diabetes + Sugar")

    # simple checks
    assert "warnings" in mock_result
    assert "alternatives" in mock_result


def test_paracetamol_alcohol():
    mock_result = {
        "warnings": ["Alcohol can increase liver damage risk with Paracetamol"],
        "alternatives": ["Avoid alcohol while taking Paracetamol"]
    }

    format_results(mock_result, case_name="Paracetamol + Alcohol")

    assert "warnings" in mock_result
    assert "alternatives" in mock_result
