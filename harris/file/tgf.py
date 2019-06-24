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

from harris.file.formatter import Formatter
from harris.unit import Unit


class Tgf(Formatter):

    def __init__(self):
        super(Tgf, self).__init__()
        self._read = False
        self._write = True

    def write(self, outfile, project, unitClass, options):
        self._file = outfile

        for unit in project.units(unitClass):
            self._writeline(str(unit.key()) + ' ' + str(unit.id()))
        self._writeline('#')
        for unit in project.units(unitClass):
            for successor in project.matrix(unitClass).successors(unit):
                self._writeline(str(unit.key()) + ' ' + str(successor.key()))
