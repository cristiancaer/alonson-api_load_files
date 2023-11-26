from django.core.exceptions import BadRequest


def get_field_from_request(request_data: dict, fieldname: str, raise_error=True):
    field = request_data.get(fieldname)
    if not field and raise_error and not isinstance(field, list):
        raise BadRequest({'detail': f'{fieldname} is required', 'type': 'body request'})
    return field


def get_field_from_url_args(request_data: dict, fieldname: str, raise_error=True):
    field = request_data.get(fieldname)
    if not field and raise_error:
        raise BadRequest({'detail': f'{fieldname} is required in url', 'type': 'dynamic url'})
    return field
