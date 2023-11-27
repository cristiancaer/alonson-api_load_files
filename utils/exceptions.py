from django.core.exceptions import BadRequest


class RecordDoesNotExist(BadRequest):
    def __init__(self, detail) -> None:
        super().__init__({'detail': detail, 'type': 'database'})


def format_db_constrain(detail):
    return {'detail': detail, 'type': 'database constraint'}


def format_serializer_errors(serializer_errors):
    if 'non_field_errors' in serializer_errors:
        return format_db_constrain(serializer_errors.get('non_field_errors')[0])
    if 'ErrorDetail' in str(serializer_errors):
        return format_field_constrain_from_serializer_error(serializer_errors)
    return {'detail': serializer_errors, 'type': 'serializer'}


def format_field_constrain(detail):
    return {'detail': detail, 'type': 'field constraint'}


def format_field_constrain_from_serializer_error(serializer_errors):
    detail = ''
    for field, error in serializer_errors.items():
        detail += f"{field}: {error[0]}\n"
    return format_field_constrain(detail)


NO_RECORDS = {'detail': 'no records for the given filters', 'type': 'database'}
TASK_DONE = {'detail': 'done', 'type': 'task status'}
