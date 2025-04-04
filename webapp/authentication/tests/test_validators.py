# webapp/authentication/tests/test_validators.py

import pytest
from authentication.validators import ContainsUppperLetterValidator
from django.core.exceptions import ValidationError


def test_valid_password_with_uppercase():
    validator = ContainsUppperLetterValidator()
    try:
        validator.validate("Password123")  # contient une majuscule
    except ValidationError:
        pytest.fail("ValidationError raised unexpectedly!")


def test_invalid_password_without_uppercase():
    validator = ContainsUppperLetterValidator()
    with pytest.raises(ValidationError):
        validator.validate("password123")  # pas de majuscule
