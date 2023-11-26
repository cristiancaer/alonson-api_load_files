import re
from django.core.exceptions import BadRequest


def validate_password(password, min_characters=8, raise_error=False):
    message = ''
    if len(password) <= min_characters:
        message = f'Password must be at least {min_characters} characters long.'
    patron = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)')
    if not bool(patron.match(password)):
        message += 'Password must contain at least one letter, one number and one special character.'
    if not message:
        return False
    if raise_error:
        raise BadRequest(message)
    return message
