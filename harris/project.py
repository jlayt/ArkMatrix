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

from harris.matrix import Matrix
from harris.unit import Unit


class Project(object):

    def __init__(self, dataset='', siteCode=''):
        self._dataset = dataset
        self._siteCode = siteCode
        self._units = {}
        self._units[Unit.Context] = {}
        self._units[Unit.Subgroup] = {}
        self._units[Unit.Group] = {}
        self._units[Unit.Landuse] = {}
        self._aggregates = {}
        self._aggregates[Unit.Subgroup] = {}
        self._aggregates[Unit.Group] = {}
        self._aggregates[Unit.Landuse] = {}
        self._matrices = {}
        self._matrices[Unit.Context] = Matrix()
        self._matrices[Unit.Subgroup] = Matrix()
        self._matrices[Unit.Group] = Matrix()

    def info(self):
        info = {}
        info['dataset'] = self._dataset
        info['siteCode'] = self._siteCode
        info['contexts'] = len(self._units[Unit.Context])
        info['subgroups'] = len(self._units[Unit.Subgroup])
        info['groups'] = len(self._units[Unit.Group])
        info['landuses'] = len(self._units[Unit.Landuse])
        info['units'] = info['contexts'] + info['subgroups'] + info['groups'] + info['landuses']
        info['orphans'] = self.orphaned(Unit.Context)
        info['missing'] = {}
        info['missing']['subgroup'] = self.unaggregated(Unit.Context)
        info['missing']['group'] = self.unaggregated(Unit.Subgroup)
        info['matrix'] = {}
        info['matrix']['context'] = self._matrices[Unit.Context].info()
        info['matrix']['subgroup'] = self._matrices[Unit.Subgroup].info()
        info['matrix']['group'] = self._matrices[Unit.Group].info()
        return info

    def isValid(self):
        """Return True if this Matrix is valid, i.e. a Directed Acyclic Graph"""
        for matrix in self._matrices.values():
            if not matrix.isValid():
                return False
        return True

    def dataset(self):
        return self._dataset

    def setDataset(self, dataset):
        self._dataset = dataset

    def siteCode(self):
        return self._siteCode

    def setSiteCode(self, siteCode):
        self._siteCode = siteCode

    def unit(self, key, unitClass):
        if str(key) in self._units[unitClass]:
            return self._units[unitClass][str(key)]
        else:
            key = self.makeKey(key)
            if key in self._units[unitClass]:
                return self._units[unitClass][key]
        return

    def units(self, unitClass):
        return sorted(self._units[unitClass].values())

    def addUnit(self, unit):
        if not unit.isValid():
            return
        self._units[unit.unitClass()][unit.key()] = unit
        if unit.unitClass() > Unit.Context and unit.key() not in self._aggregates[unit.unitClass()]:
            self._aggregates[unit.unitClass()][unit.key()] = {}
        if unit.aggregate():
            aggregate = unit.aggregate()
            self._aggregates[aggregate.unitClass()][aggregate.key()][unit.key()] = unit

    def hasUnit(self, unit, unitClass=Unit.Context):
        if isinstance(unit, Unit):
            return unit.key() in self._units[unit.unitClass()].keys()
        return unit in self._units[unitClass].keys() or self.makeKey(unit) in self._units[unitClass].keys()

    def removeUnit(self, unit):
        self._matrices[unit.unitClass()].removeUnit(unit)
        self._units[unit.unitClass()].pop(unit.key())
        if unit.aggregate():
            aggregate = unit.aggregate()
            self._aggregates[aggregate.unitClass()][aggregate.key()].pop(unit.key())

    def addRelationship(self, fromUnit, reln, toUnit):
        if (fromUnit.unitClass() == toUnit.unitClass()):
            self._matrices[fromUnit.unitClass()].addRelationship(fromUnit, reln, toUnit)

    def addRelationships(self, fromUnit, reln, toUnits):
        self._matrices[fromUnit.unitClass()].addRelationship(fromUnit, reln, toUnits)

    def orphaned(self, unitClass):
        units = []
        for unit in self._units[unitClass].values():
            if unit not in self._matrices[unitClass]:
                units.append(unit)
        return sorted(units)

    def removeOrphans(self, unitClass):
        units = self.orphaned(unitClass)
        for unit in units:
            self.removeUnit(unit)

    def addAggregate(self, unit, aggregate):
        self.addUnit(aggregate)
        unit.setAggregate(aggregate)
        self.addUnit(unit)
        self._aggregates[aggregate.unitClass()][aggregate.key()][unit.key()] = unit

    def unaggregated(self, unitClass):
        units = []
        for unit in self._units[unitClass].values():
            if unit.aggregate() is None:
                units.append(unit)
        return sorted(units)

    def makeKey(self, unitId):
        unitId = str(unitId)
        if self._siteCode and unitId:
            return self._siteCode + '_' + unitId
        return unitId

    def matrix(self, unitClass):
        return self._matrices[unitClass]

    def generateAggregateMatrix(self, unitClass):
        self._matrices[unitClass].clear()
        if len(self._aggregates[unitClass]) == 0:
            return
        for reln in self.matrix(unitClass - 1).relationships():
            ag1 = self.unit(reln[0], unitClass - 1).aggregate()
            ag2 = self.unit(reln[1], unitClass - 1).aggregate()
            if ag1 and ag2 and ag1 != ag2:
                self._matrices[unitClass].addRelationship(ag1, Matrix.Above, ag2)
        self._matrices[unitClass].reduce()
        return self._matrices[unitClass]

    def redundantUnits(self):
        return self._matrices[Unit.Context].redundantUnits()

    def redundantRelationships(self):
        return self._matrices[Unit.Context].redundantRelationships()

    def resolve(self):
        self._matrices[Unit.Context].resolve()

    def reduce(self):
        return self._matrices[Unit.Context].reduce()

    def aggregate(self):
        for unitClass in range(Unit.Subgroup, Unit.Landuse):
            self.generateAggregateMatrix(unitClass)

    def simplify(self):
        redundant = self._matrices[Unit.Context].simplify()
        for unit in redundant:
            self.removeUnit(unit)
