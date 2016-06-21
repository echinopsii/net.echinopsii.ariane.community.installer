# CC installer configuration parameter interface
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
from zope.interface import Interface, Attribute

__author__ = 'mffrench'


class IConfParam(Interface):
    """Ariane configuration parameter interface"""
    name = Attribute("""The CC parameter name which must be pushed into final configuration file.
                                       The param name must same as the templated configuration param. """)
    value = Attribute("""The CC parameter value.""")
    description = Attribute("""The CC parameter description.""")
    hide = Attribute("""Tell if parameter value must be hided or not""")

    def is_valid(self):
        """Check if the value of this configuration is valid"""



