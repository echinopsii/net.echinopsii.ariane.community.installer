# CC installer conf unit interface
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
import zope.interface

__author__ = 'mffrench'


class IConfUnit(zope.interface.Interface):
    """CC configuration unit interface"""
    confUnitName = zope.interface.Attribute("""the CC configuration unit name""")
    confTemplatePath = zope.interface.Attribute("""the CC configuration template to change""")
    confFinalPath = zope.interface.Attribute("""the CC final configuration to generate""")
    paramsDictionary = zope.interface.Attribute("""the CC configuration parameters dictionary""")

    def getParamsKeysList(self):
        """Get the configuration parameters keys list of this configuration unit"""

    def getParamFromKey(self, key):
        """Get the configuration parameter from its key"""

    def setKeyParamValue(self, key, param):
        """Set the value of param defined by its key. If the value is invalid an exception is raised"""

    def process(self):
        """Process template configuration to setup final configuration with provided parameters"""




