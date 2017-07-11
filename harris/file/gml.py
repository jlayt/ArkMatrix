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

from harris.unit import Unit
from harris.matrix import Matrix
from harris.utilities import *

class Gml():

    def write(self, project, unitClass, options):

        self._writeHeader()

        for unit in project.units(unitClass):
            if options['aggregate']:
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

    def writeSubgroup(self, project, options):

        self._writeHeader()

        for subgroup in project.units(Unit.Subgroup).values():
            self._writeNode(subgroup.node(), subgroup.id(), '', options['style'], options['width'], options['height'])

        eid = 0
        for edge in project.matrix(Unit.Subgroup).relationships():
            self._writeEdge(eid, edge[0].node(), edge[1].node(), options['style'])
            eid += 1

        if options['aggregate']:
            for unit in project.units(Unit.Group):
                self._writeAggregate(unit.node(), unit.id(), 'Group')

        self._writeFooter()

    def writeGroup(self, project, options):

        self._writeHeader()

        for group in project.units(Unit.Group).values():
            self._writeNode(group.node(), group.id(), '', options['style'], options['width'], options['height'])

        eid = 0
        for edge in project.matrix(Unit.Group).relationships():
            self._writeEdge(eid, edge[0].node(), edge[1].node(), options['style'])
            eid += 1

        self._writeFooter()

    def _writeHeader(self):
        print 'graph ['
        print '    directed 1'

    def _writeFooter(self):
        print ']'

    def _writeNode(self, nodeId, unitId, groupId, style, width, height):
        print '    node ['
        print '        id ' + str(nodeId)
        print '        label ' + doublequote(unitId)
        if style:
            print '        graphics ['
            print '            type "rectangle"'
            print '            w ' + str(width)
            print '            h ' + str(height)
            print '        ]'
        if groupId:
            print '        gid ' + str(groupId)
        print '    ]'

    def _writeAggregate(self, nodeId, unitId, name):
        print '    node ['
        print '        id ' + str(nodeId)
        print '        label ' + doublequote(name + ' ' + unitId)
        print '        isGroup 1'
        print '    ]'

    def _writeEdge(self, edgeId, fromNodeId, toNodeId, style):
        print '    edge ['
        print '        id ' + str(edgeId)
        print '        source ' + str(fromNodeId)
        print '        target ' + str(toNodeId)
        if style:
            print '        graphics ['
            print '            arrow "none"'
            print '        ]'
        print '    ]'
