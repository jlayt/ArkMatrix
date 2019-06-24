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
from harris.matrix import Matrix
from harris.utilities import *


class Gxl(Formatter):

    def __init__(self):
        super(Gxl, self).__init__()
        self._read = False
        self._write = True

    def write(self, outfile, project, unitClass, options):
        self._file = outfile

        self._writeline('<?xml version="1.0" encoding="UTF-8"?>')
        self._writeline('<!DOCTYPE gxl SYSTEM "http://www.gupro.de/GXL/gxl-1.0.dtd">')

        self._writeline('<gxl xmlns:xlink=" http://www.w3.org/1999/xlink">')
        self._writeline('    <graph id="' + project.dataset() + '" edgeids="true" edgemode="directed">')

        for unit in project.units(unitClass):
            self._writeline('        <node id=' + doublequote(unit.id()) + '/>')

        eid = 0
        for edge in project.matrix(unitClass).relationships():
            frm = edge[0]
            to = edge[1]
            self._writeline('        <edge id=' + doublequote(eid) + ' from="' + doublequote(edge[0].id())
                             + ' to=' + doublequote(edge[1].id()) + '/>')
            eid += 1

        self._writeline('    </graph>')
        self._writeline('</gxl>')
