# installer bus processor
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
from core.bus.CUBusProcessor import BusSyringe

__author__ = 'mffrench'


class BusProcessor:

    def __init__(self, dist_version, dist_dep_type, silent):
        print("\n%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--"
              "%--%--%--%--%--%--%--%--%--\n")
        print("%-- Bus configuration : \n")
        self.silent = silent
        self.dist_version = dist_version
        self.dist_dep_type = dist_dep_type

        self.busSyringe = BusSyringe(self.dist_version, self.silent)
        self.busSyringe.shoot_builder()

    def process(self, template_path, conf_final_path):
        self.busSyringe.set_conf_template_path(template_path)
        self.busSyringe.set_conf_final_path(conf_final_path)
        self.busSyringe.inject()
        return self
