from dataclasses import dataclass, field
from .models import TransactionFile, TransactionColumnNameOption, Transaction
from utils.files import get_file_extension, PLAIN_EXTENSIONS, EXCEL_EXTENSIONS
import pandas as pd
import numpy as np
from django.core.files.uploadhandler import FileUploadHandler
from utils.fields import format_as_key_name, str_to_bool
from typing import Dict, List


@dataclass
class TransactionsHandler:
    transaction_file: TransactionFile
    file_handler: FileUploadHandler  # use from request rather transaction_file-model to avoid download file from azure
    df: pd.DataFrame = field(init=False)
    found_columns: Dict[str, str] = field(default_factory=dict)
    COLUMN_NAMES_OPTIONS: Dict[str, List[str]] = field(init=False)
    DF_OPTIONS = {
                'skiprows': 7,
                # 'index_col': 0,
                # 'skipfooter': 2
            }

    def get_column_names_options(self):
        query = TransactionColumnNameOption.objects.all()
        column_names_options = {}
        for column in query:
            column.values = [format_as_key_name(value) for value in column.values]
            column_names_options.update({column.key_name: column})
        return column_names_options

    def format_columns(self, columns):
        def format_column(column):
            format_column = format_as_key_name(column)
            for key, column_data in self.COLUMN_NAMES_OPTIONS.items():
                if format_column in column_data.values:
                    self.found_columns.update({key: column})
                    return key
            return format_column
        return [format_column(column) for column in columns]

    def delete_unnecessary_columns(self, df):
        columns = set(df.columns)
        expected_columns = set(self.COLUMN_NAMES_OPTIONS.keys())
        unnecessary_columns = columns - expected_columns
        return df.drop(columns=unnecessary_columns)

    def check_df_columns(self, df):
        df_columns = set(df.columns)
        required_columns = {column.key_name for column in self.COLUMN_NAMES_OPTIONS.values() if column.is_required}
        missing_columns = required_columns - df_columns
        message = ''
        for column in missing_columns:
            message += f" Columna {column} es necesaria. options: {self.COLUMN_NAMES_OPTIONS.get(column)}\n"
        if message:
            raise Exception(message)

    def __post_init__(self):
        self.COLUMN_NAMES_OPTIONS = self.get_column_names_options()
        self.df = self.get_df()

    def format_data_frame(self, df):
        # df = df.dropna(how='all', axis=1)  # Drop columns with all NaN values
        df.columns = self.format_columns(df.columns)
        df = self.delete_unnecessary_columns(df)
        self.check_df_columns(df)
        df = df.replace(np.nan, None)
        df['is_transactional'] = [str_to_bool(value) for value in df['is_transactional']]
        return df

    def get_df(self):
        extension = get_file_extension(self.transaction_file.file.name)
        if extension not in PLAIN_EXTENSIONS + EXCEL_EXTENSIONS:
            raise Exception('invalid file')
        if extension in PLAIN_EXTENSIONS:
            df = pd.read_csv(self.file_handler, **self.DF_OPTIONS)
        else:
            df = pd.read_excel(self.file_handler, **self.DF_OPTIONS)
        df = self.format_data_frame(df)
        return df

    def row_to_transaction(self, row, index):
        def check_value(value, column, index):
            if value is None and self.COLUMN_NAMES_OPTIONS.get(column).is_required:
                raise Exception(f"Celda requerida, vacía: fila {index + self.DF_OPTIONS.get('skiprows') + 2}, columna {self.found_columns.get(column)}")
            return value
        row = {key: check_value(value, key, index) for key, value in row.items()}
        return Transaction(**row, index_in_file=index, version=self.transaction_file.last_version, is_adjustment=self.transaction_file.is_adjustment, file=self.transaction_file)

    def save_in_db(self):
        self.transaction_file.transactions.all().update(is_active=False)
        transactions_to_save = [self.row_to_transaction(row, index) for index, row in self.df.iterrows()]
        Transaction.objects.bulk_create(transactions_to_save)
