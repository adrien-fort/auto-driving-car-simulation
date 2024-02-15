from src.field import Field

import pytest
from unittest.mock import patch

@pytest.mark.parametrize("input_values, expected_result", [
    (['10 20'], (10, 20)),
    (['abc', '3 4 5', '10 ten', '1 2'], (1, 2)),
])
def test_field_creation(input_values, expected_result, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: input_values.pop(0))
    field_instance = Field(None, None)
    new_field_instance = field_instance.field_creation()
    assert new_field_instance.width == expected_result[0]
    assert new_field_instance.height == expected_result[1]
