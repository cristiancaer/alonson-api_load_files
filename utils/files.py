import pathlib


PLAIN_EXTENSIONS = ['csv', 'txt']
EXCEL_EXTENSIONS = ['xlsx', 'xls']


def get_file_extension(filename):
    return pathlib.Path(filename).suffix.strip('.')