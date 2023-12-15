import re
from django.core.exceptions import BadRequest
from django.core.validators import MaxValueValidator, MinValueValidator
import unicodedata


def setRangeValidators(min_value, max_value):
    return (MinValueValidator(min_value), MaxValueValidator(max_value))


def validate_password(password, min_characters=8, raise_error=False):
    message = ''
    if len(password) < min_characters:
        message = f'Password must be at least {min_characters} characters long.'
    patron = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)')
    if not bool(patron.match(password)):
        message += 'Password must contain at least one letter and one number.'
    if not message:
        return False
    if raise_error:
        raise BadRequest(message)
    return message


def replace_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii.decode()


def format_as_key_name(input_str):
    return replace_accents(input_str).lower().strip().strip(' ')


def str_to_bool(value):
    if not value:
        return False
    value = format_as_key_name(value)
    if value in ('yes', 'true', 't', 'y', '1', 'si', 's'):
        return True
    return False
