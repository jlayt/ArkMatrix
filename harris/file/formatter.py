# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK Matrix
      Part of the Archaeological Recording Kit by L - P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
                    Copyright : 2018 John Layt
                    Copyright : 2018 L - P : Heritage LLP
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This file is part of ARK Matrix.                                      *
 *                                                                         *
 *   ARK Matrix is free software: you can redistribute it and/or modify    *
 *   it under the terms of the GNU Lesser General Public License as        *
 *   published by the Free Software Foundation, either version 3 of the    *
 *   License, or (at your option) any later version.                       *
 *                                                                         *
 *   ARK is distributed in the hope that it will be useful,                *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the          *
 *   GNU Lesser General Public License for more details.                   *
 *                                                                         *
 *   You should have received a copy of the GNU Lesser General Public      *
 *   License along with ARK Matrix. If not, see                            *
 *   <http://www.gnu.org/licenses/>.                                       *
 *                                                                         *
 ***************************************************************************/
"""

from harris.unit import Unit


class Formatter(object):

    def __init__(self):
        self._read = False
        self._write = False
        self._file = None

    def canRead(self):
        return self._read

    def canWrite(self):
        return self._write

    def read(self, infile, dataset='', siteCode=''):
        return

    def write(self, outfile, project, unitClass, options):
        return

    def _writeline(self, line):
        if self._file:
            self._file.write(str(line) + '\n')

    def _unit(self, project, unitId, unitClass):
        if project.hasUnit(unitId, unitClass):
            return project.unit(unitId, unitClass)
        unit = Unit(project.siteCode(), unitId, unitClass)
        project.addUnit(unit)
        return unit
