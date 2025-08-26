# core/validators.py
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class CollegeEmailValidator(EmailValidator):
    """
    Validates that the email address ends with the specific college domain.
    This ensures only users with official college emails can register.
    """
    def __init__(self, domain='jainuniversity.ac.in', **kwargs):
        # Create a regex pattern that matches the end of the string
        # The r'\.[a-z]{2,}$' part matches the TLD (like .ac.in)
        self.domain_pattern = r'@' + domain.replace('.', r'\.') + '$'
        super().__init__(**kwargs)  # Initialize the parent EmailValidator

    def __call__(self, value):
        # First, run the standard email validation (checks for @, format, etc.)
        super().__call__(value)
        
        # Now, check for our specific domain
        import re
        if not re.search(self.domain_pattern, value, re.IGNORECASE):
            raise ValidationError(
                _('Email must be an official Jain University address (%(domain)s).'),
                code='invalid_college_domain',
                params={'domain': '@jainuniversity.ac.in'},
            )