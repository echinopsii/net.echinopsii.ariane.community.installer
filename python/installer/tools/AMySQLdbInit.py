# CC installer MySQL db init abstract class
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
from abc import abstractmethod
import re
import mysql.connector
from mysql.connector import OperationalError, ProgrammingError, DatabaseError
from zope.interface import implementer
from tools.ISQLdbInit import ISQLdbInit


__author__ = 'mffrench'


@implementer(ISQLdbInit)
class AMySQLdbInit:

    @staticmethod
    def exec_sql_file(cursor, sql_file):
        statement = ""
        for line in sql_file:
            if re.match(r'--', line):  # ignore sql comment lines
                continue
            if not re.search(r'[^-;]+;', line):  # keep appending lines that don't end in ';'
                statement += line
            else:  # when you get a line ending in ';' then exec statement and reset for next statement
                statement += line
                #print("Executing SQL statement:\n%s" % (statement))
                try:
                    cursor.execute(statement)
                except (DatabaseError, OperationalError, ProgrammingError) as err:
                    print("Error: {0}".format(err))

                statement = ""

    @abstractmethod
    def process(self):
        try:
            sqlScriptFile = open(self.sqlScriptFilePath, "r")
        except OSError as err:
            print("OS error: {0}".format(err))
            raise

        cnx = mysql.connector.connect(
            user=self.dbServerUser,
            password=self.dbServerPassword,
            host=self.dbServerHost,
            port=self.dbServerPort,
            database=self.dbName
        )
        cursor = cnx.cursor()
        AMySQLdbInit.exec_sql_file(cursor, sqlScriptFile)
