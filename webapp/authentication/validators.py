from django.core.exceptions import ValidationError


class ContainsUppperLetterValidator:
    def validate(self, password, user=None):
        if not any(char.isupper() for char in password):
            raise ValidationError(
                'Password must contain at least 1 upper letter',
                code='password_no_upper_letter'
            )

    def get_help_text(self):
        return "Password must contains at least 1 uppper letter"
