# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK Matrix
        Part of the Archaeological Recording Kit by L-P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        begin                : 2016-02-29
        git sha              : $Format:%H$
        copyright            : 2016 by John Layt
        email                : john@layt.net
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import zlib

from harris.file.format import Format
from harris.unit import Unit
from harris.matrix import Matrix
from harris.utilities import *

class Gml(Format):

    def write(self, outfile, project, unitClass, options):
        self._file = outfile
        self._writeHeader()

        for unit in project.units(unitClass):
            if options['aggregate'] and unit.aggregate():
                gid = unit.aggregate().node()
            else:
                gid = ''

            self._writeNode(unit.node(), unit.id(), gid, options['style'], options['width'], options['height'])

        eid = 0
        for edge in project.matrix(Unit.Context).relationships():
            frm = edge[0]
            to = edge[1]
            self._writeEdge(eid, edge[0].node(), edge[1].node(), options['style'])
            eid += 1

        if options['aggregate']:
            for unit in project.units(Unit.Subgroup):
                self._writeAggregate(unit.node(), unit.id(), 'Subgroup')

        self._writeFooter()
        self._file = None

    def _writeHeader(self):
        self._writeline('graph [')
        self._writeline('    directed 1')

    def _writeFooter(self):
        self._writeline(']')

    def _writeNode(self, nodeId, unitId, groupId, style, width, height):
        self._writeline('    node [')
        self._writeline('        id ' + str(nodeId))
        self._writeline('        label ' + doublequote(unitId))
        if style:
            self._writeline('        graphics [')
            self._writeline('            type "rectangle"')
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
