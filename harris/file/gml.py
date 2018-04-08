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

import zlib

from harris.file.formatter import Formatter
from harris.unit import Unit
from harris.matrix import Matrix
from harris.utilities import *


class Gml(Formatter):

    def __init__(self):
        super(Gml, self).__init__()
        self._read = False
        self._write = True

    def write(self, outfile, project, unitClass, options):
        self._file = outfile
        self._writeHeader()

        aggregate = options.get('aggregate', False)
        style = options.get('style', True)
        width = options.get('width', 50)
        height = options.get('height', 25)

        for unit in project.units(unitClass):
            if aggregate and unit.aggregate():
                gid = unit.aggregate().node()
            else:
                gid = ''

            self._writeNode(unit.node(), unit.id(), unit.label(), gid, style, width, height)

        eid = 0
        for edge in project.matrix(Unit.Context).relationships():
            frm = edge[0]
            to = edge[1]
            self._writeEdge(eid, edge[0].node(), edge[1].node(), style)
            eid += 1

        if aggregate:
            for unit in project.units(Unit.Subgroup):
                self._writeAggregate(unit.node(), unit.id(), 'Subgroup')

        self._writeFooter()
        self._file = None

    def _writeHeader(self):
        self._writeline('graph [')
        self._writeline('    directed 1')

    def _writeFooter(self):
        self._writeline(']')

    def _writeNode(self, nodeId, unitId, label, groupId, style, width, height):
        self._writeline('    node [')
        self._writeline('        id ' + str(nodeId))
        self._writeline('        label ' + doublequote(label))
        if style:
            self._writeline('        graphics [')
            self._writeline('            type "rectangle"')
            self._writeline('            hasFill 0')
            self._writeline('            w ' + str(width))
            self._writeline('            h ' + str(height))
            self._writeline('        ]')
        if groupId:
            self._writeline('        gid ' + str(groupId))
        self._writeline('    ]')

    def _writeAggregate(self, nodeId, unitId, name):
        self._writeline('    node [')
        self._writeline('        id ' + str(nodeId))
        self._writeline('        label ' + doublequote(name + ' ' + unitId))
        self._writeline('        isGroup 1')
        self._writeline('    ]')

    def _writeEdge(self, edgeId, fromNodeId, toNodeId, style):
        self._writeline('    edge [')
        self._writeline('        id ' + str(edgeId))
        self._writeline('        source ' + str(fromNodeId))
        self._writeline('        target ' + str(toNodeId))
        if style:
            self._writeline('        graphics [')
            self._writeline('            arrow "none"')
            self._writeline('        ]')
        self._writeline('    ]')
