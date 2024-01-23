# create a static method to validate if file with date today exists

import os
import datetime
from utils.dir import make_dir
from django.conf import settings


class BaseLog:
    log_path: settings.BASE_DIR
    file_name = 'log'

    @classmethod
    def get_path_name(self):
        make_dir(self.log_path)  # only will create it if the path does not exist
        self.today = datetime.date.today()
        self.file_path_name = os.path.join(self.log_path, str(self.today) + '_' + self.file_name + '.log').replace('\\', '/')
        return self.file_path_name

    @classmethod
    def exists(self):
        return os.path.isfile(self.get_path_name())

    @classmethod
    def create(self):
        file = open(self.get_path_name(), 'w')
        file.close()

    @classmethod
    def write(self, message):

        if not self.exists():
            self.create()

        file = open(self.get_path_name(), 'a')
        now = str(datetime.datetime.now())
        file.write(f'{now} :{message} \n')
        file.close()

    @classmethod
    def error(self, message):
        self.write(f'error: {message}')

    @classmethod
    def warning(self, message):
        self.write(f'warning: {message}')
