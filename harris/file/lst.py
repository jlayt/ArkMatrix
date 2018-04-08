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
from harris.project import Project
from harris.unit import Unit
from harris.matrix import Matrix
from harris.utilities import *


class Lst(Formatter):

    # Temp default site code
    _siteCode = ''

    def __init__(self):
        super(Lst, self).__init__()
        self._read = True
        self._write = False

    def read(self, infile, dataset='', siteCode=''):
        project = Project(dataset, siteCode)
        line = infile.readline().strip()
        project.dataset = line.strip()[len('Stratigraphic Dataset'):].strip()
        self._siteCode = project.siteCode()
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
        unitClass = Unit.Context
        for line in infile:
            if (line.strip() == ''):
                pass
            elif (not line.startswith(' ')):
                if unitId:
                    self._addUnit(project, unitClass, site, unitId, groupId, above, below, contemporary, equal)
                site, unitId = self._lstNameToUnit(line.strip())
                groupId = ''
                above = []
                contemporary = []
                equal = []
                below = []
                unitClass = Unit.Context
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
                    unitClass = attribute[len('unit class:'):].strip()
                    unitClass = Unit.Class.index(unitClass)

        self._addUnit(project, unitClass, site, unitId, groupId, above, below, contemporary, equal)
        return project

    def _addUnit(self, project, unitClass, site, unitId, groupId, aboves, belows, contemporaries, equals):
        if unitId:
            if unitClass == Unit.Context:
                unit = self._unit(project, unitId, unitClass)
                project.addUnit(unit)
                for belowId in belows:
                    below = self._unit(project, belowId, unitClass)
                    project.addRelationship(unit, Matrix.Above, below)
                for equalId in equals:
                    equal = self._unit(project, equalId, unitClass)
                    project.addRelationship(unit, Matrix.Same, equal)
                for contemporaryId in contemporaries:
                    contemporary = self._unit(project, contemporaryId, unitClass)
                    project.addRelationship(unit, Matrix.Contemporary, contemporary)
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
