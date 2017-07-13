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

from harris.project import Project
from harris.unit import Unit
from harris.matrix import Matrix
from harris.utilities import *

class Lst():

    # Temp default site code
    _siteCode = ''

    def read(self, infile, dataset = '', siteCode = ''):
        project = Project(dataset, siteCode)
        line = infile.readline().strip()
        project.dataset = line.strip()[len('Stratigraphic Dataset'):].strip()
        self._siteCode = project.siteCode
        if not project.dataset:
            project.dataset = 'harris'
        line = infile.readline().strip()
        line = infile.readline().strip()
        site = ''
        unitId = ''
        groupId = ''
        above = []
        contemporary = []
        equal = []
        below = []
        unit = 'context'
        for line in infile:
            if (line.strip() == ''):
                pass
            elif (not line.startswith(' ')):
                if unitId:
                    self._addUnit(project, unit, site, unitId, groupId, above, below, contemporary, equal)
                site, unitId = self._lstNameToUnit(line.strip())
                groupId = ''
                above = []
                contemporary = []
                equal = []
                below = []
                unit = 'context'
            else:
                attribute = line.strip()
                if (attribute.lower().startswith('above:')):
                    above.extend(self._lstKeyList(attribute, 'above:'))
                elif (attribute.lower().startswith('contemporary with:')):
                    contemporary.extend(self._lstKeyList(attribute, 'contemporary with:'))
                elif (attribute.lower().startswith('equal to:')):
                    equal.extend(self._lstKeyList(attribute, 'equal to:'))
                elif (attribute.lower().startswith('below:')):
                    below.extend(self._lstKeyList(attribute, 'below:'))
                elif (attribute.lower().startswith('part of:')):
                    groupId = attribute[len('part of:'):].strip()
                elif (attribute.lower().startswith('unit class:')):
                    unit = attribute[len('unit class:'):].strip()

        self._addUnit(project, unit, site, unitId, groupId, above, below, contemporary, equal)

    def _addUnit(self, project, unit, site, unitId, groupId, above, below, contemporary, equal):
        if unitId:
            if unit == 'context':
                unit = Unit(site, unitId, groupId, Unit.Assigned)
                project.addUnit(unit)
                project.matrix.addRelationships(unit.key(), Matrix.Above, below)
                project.matrix.addRelationships(unit.key(), Matrix.SameAs, equal)
                project.matrix.addRelationships(unit.key(), Matrix.ContemporaryWith, contemporary)
                if groupId:
                    project.addSubgrouping(groupId, unitId)

    def _lstNameToUnit(self, name):
        components = name.split('::')
        if len(components) > 1:
            return components[0], components[1]
        return self._siteCode, components[0]

    def _lstNameToKey(self, name):
        site, unitId = self._lstNameToUnit(name)
        if site:
            return site + '_' + unitId
        else:
            return unitId

    def _lstKeyList(self, input, tag):
        names = input[len(tag):].strip().replace(',', ' ').split()
        return [self._lstNameToKey(name) for name in names]
