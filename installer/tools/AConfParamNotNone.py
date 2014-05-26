# CC installer configuration param not None abstract class
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
import sys
from zope.interface import implementer
from tools.IConfParam import IConfParam

__author__ = 'mffrench'


@implementer(IConfParam)
class AConfParamNotNone:

    @abstractmethod
    def isValid(self):
        if self.value is None:
            print(self.description + " is not defined !", file=sys.stderr)
            return False
        else:
            return True