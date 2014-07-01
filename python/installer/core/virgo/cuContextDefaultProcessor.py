# installer - context default
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
import json
import os
from tools.AConfParamNotNone import AConfParamNotNone
from tools.AConfUnit import AConfUnit

__author__ = 'mffrench'


class cpVirgoHome(AConfParamNotNone):

    name = "##KERNEL_HOME"
    description = "Virgo Home"
    hide = False

    def __init__(self):
        self.value = None


class cuContextDefaultProcessor(AConfUnit):

    def __init__(self, targetConfDir):
        self.confUnitName = "Virgo Context Default "
        self.confTemplatePath = os.path.abspath("resources/templates/virgo/context.xml.default.tpl")
        self.confFinalPath = targetConfDir + "context.xml.default"
        virgoHome = cpVirgoHome()
        self.paramsDictionary = {
            virgoHome.name: virgoHome
        }


class contextDefaultSyringe:

    def __init__(self, targetConfDif, virgoHome):
        self.contextDefaultCUProcessor = cuContextDefaultProcessor(targetConfDif)
        self.contextDefaultCUProcessor.setKeyParamValue(cpVirgoHome.name, virgoHome)

    def inject(self):
        self.contextDefaultCUProcessor.process()