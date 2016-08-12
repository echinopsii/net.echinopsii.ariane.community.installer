# CC installer configuration unit abstract class
#
# Copyright (C) 2014 Mathilde Ffrench
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from abc import ABCMeta, abstractmethod
import os
import shutil
from zope.interface import implementer
from tools.IConfUnit import IConfUnit

__author__ = 'mffrench'

@implementer(IConfUnit)
class AConfUnit:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_params_keys_list(self):
        return self.paramsDictionary.keys()

    @abstractmethod
    def get_param_from_key(self, key):
        return self.paramsDictionary[key]

    @abstractmethod
    def set_key_param_value(self, key, value):
        self.paramsDictionary[key].value = value
        if not self.paramsDictionary[key].is_valid():
            self.paramsDictionary[key].value = None
            raise Exception("Invalid value " + str(value) + " for parameter " + key)

    @abstractmethod
    def process(self):
        print("\n%-- [INFO] " + self.confUnitName + " configuration processing is starting")
        new_template_file_path = None
        if self.confTemplatePath == self.confFinalPath:
            new_template_file_path = self.confFinalPath + ".tpl"
            shutil.copy(self.confFinalPath, new_template_file_path)

        try:
            if new_template_file_path is not None:
                template_file = open(new_template_file_path, "r")
            else:
                template_file = open(self.confTemplatePath, "r")
        except OSError as err:
            print("OS error: {0}".format(err))
            raise

        try:
            final_file = open(self.confFinalPath, "w")
        except OSError as err:
            print("OS error: {0}".format(err))
            raise

        for line in template_file:
            for key in self.paramsDictionary.keys():
                if line.__contains__(key):
                    value = self.paramsDictionary[key].value
                    if value is not None and value != "":
                        if self.paramsDictionary[key].hide:
                            print("%-- [INFO] " + self.paramsDictionary[key].description + " : *****")
                        else:
                            print("%-- [INFO] " + self.paramsDictionary[key].description + " : " + str(value))
                        line = line.replace(key, str(value))
                    else:
                        line = ""
            final_file.write(line)

        template_file.close()
        final_file.close()

        if new_template_file_path is not None:
            os.remove(new_template_file_path)

        print("%-- [INFO] " + self.confUnitName + " configuration processing has been done successfully\n")
