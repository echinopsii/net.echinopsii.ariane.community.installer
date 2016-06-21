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
import os
from tools.AConfParamNotNone import AConfParamNotNone
from tools.AConfUnit import AConfUnit

__author__ = 'mffrench'


class CPVirgoHome(AConfParamNotNone):

    name = "##KERNEL_HOME"
    description = "Virgo Home"
    hide = False

    def __init__(self):
        self.value = None

    def is_valid(self):
        return super(CPVirgoHome, self).is_valid()


class CUContextDefaultProcessor(AConfUnit):

    def __init__(self, target_conf_dir):
        self.confUnitName = "Virgo Context Default "
        self.confTemplatePath = os.path.abspath("resources/templates/virgo/context.xml.default.tpl")
        self.confFinalPath = target_conf_dir + "/context.xml.default"
        virgo_home = CPVirgoHome()
        self.paramsDictionary = {
            virgo_home.name: virgo_home
        }

    def process(self):
        return super(CUContextDefaultProcessor, self).process()

    def get_param_from_key(self, key):
        return super(CUContextDefaultProcessor, self).get_param_from_key(key)

    def get_params_keys_list(self):
        return super(CUContextDefaultProcessor, self).get_params_keys_list()

    def set_key_param_value(self, key, value):
        return super(CUContextDefaultProcessor, self).set_key_param_value(key, value)


class ContextDefaultSyringe:

    def __init__(self, target_conf_dir, virgo_home):
        self.contextDefaultCUProcessor = CUContextDefaultProcessor(target_conf_dir)
        self.contextDefaultCUProcessor.set_key_param_value(CPVirgoHome.name, virgo_home)

    def inject(self):
        self.contextDefaultCUProcessor.process()
