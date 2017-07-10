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

    def write(self, project, options):

        self._writeHeader()

        for unit in project.units():
            if options['group']:
                gid = unit.aggregate()._nid
            else:
                gid = ''

            self._writeNode(unit._nid, unit.unitId(), gid, options['style'], options['width'], options['height'])

        eid = 0
        for edge in project.matrix._strat.edges_iter():
            self._writeEdge(eid, project.unit(edge[0])._nid, project.unit(edge[1])._nid, options['style'])
            eid += 1

        if options['group']:
            for unit in project._subgroups:
                self._writeAggregate(unit._nid, unit.unitId(), 'Subgroup')

        self._writeFooter()

    def writeSubgroup(self, project, options):

        self._writeHeader()

        for subgroupId in project._subgroups.keys():
            self._writeNode(self._hash(subgroupId), subgroupId, '', options['style'], options['width'], options['height'])

        eid = 0
        for edge in project.subgroupMatrix._strat.edges_iter():
            self._writeEdge(eid, self._hash(edge[0]), self._hash(edge[1]), options['style'])
            eid += 1

        self._writeFooter()

    def writeGroup(self, project, options):

        self._writeHeader()

        for groupId in project._groups.keys():
            self._writeNode(self._hash(groupId), groupId, '', options['style'], options['width'], options['height'])

        eid = 0
        for edge in project.groupMatrix._strat.edges_iter():
            self._writeEdge(eid, self._hash(edge[0]), self._hash(edge[1]), options['style'])
            eid += 1

        self._writeFooter()

    def _hash(self, value):
        return zlib.adler32(value) & 0xffffffff

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
