# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK Matrix
        Part of the Archaeological Recording Kit by L-P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        begin                : 2016-02-29
        git sha              : $Format:%H$
        copyright            : 2017 by John Layt
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

import csv

from harris.file.formatter import Formatter
from harris.project import Project
from harris.unit import Unit
from harris.matrix import Matrix
from harris.utilities import *

class Csv(Formatter):

    def __init__(self):
        self._read = True
        self._write = True

    def read(self, infile, dataset = '', siteCode = ''):
        project = Project(dataset, siteCode)
        reader = csv.reader(infile)
        prevTarget = None
        for record in reader:
            #try:
                source = str(record[0])
                target = str(record[1])
                if len(record) >= 3:
                    tag = str(record[2])
                else:
                    tag = 'above'
                if tag == 'site':
                    project.setSiteCode(source)
                    continue
                if tag == 'dataset':
                    project.setDataset(source)
                    continue
                if tag == 'type':
                    if target in Unit.Type:
                        unit = self._unit(project, source, Unit.Context)
                        unit.setType(Unit.Class.index(target))
                    continue
                if tag == 'status':
                    if source and target in Unit.Status:
                        # TODO Status of subgroup/group/landuse?
                        unit = self._unit(project, source, Unit.Context)
                        unit.setStatus(Unit.Status.index(target))
                    continue
                if tag == 'label':
                    if source and target:
                        unit = self._unit(project, source, Unit.Context)
                        unit.setLabel(target)
                    continue
                if tag == 'group':
                    if source and target:
                        subgroup = self._unit(project, source, Unit.Subgroup)
                        group = self._unit(project, target, Unit.Group)
                        project.addAggregate(subgroup, group)
                elif tag == 'subgroup':
                    if source and target:
                        context = self._unit(project, source, Unit.Context)
                        subgroup = self._unit(project, target, Unit.Subgroup)
                        project.addAggregate(context, subgroup)
                elif tag in Matrix.Relationship:
                    if not source:
                        source = prevTarget
                    prevTarget = target
                    if source and target:
                        source = self._unit(project, source, Unit.Context)
                        target = self._unit(project, target, Unit.Context)
                        project.addRelationship(source, Matrix.Relationship.index(tag), target)
            #except:
                #if record:
                    #print 'Error reading row: ' + str(record)
        return project

    def _unit(self, project, unitId, unitClass):
        if project.hasUnit(unitId, unitClass):
            return project.unit(unitId, unitClass)
        unit = Unit(project.siteCode(), unitId, unitClass)
        project.addUnit(unit)
        return unit

    def write(self, outfile, project, unitClass, options):
        self._file = outfile
        self._print(project.siteCode(), '', 'site')
        self._print(project.dataset(), '', 'dataset')
        for unit in project.units(unitClass):
            if unit.type() != Unit.Undefined:
                self._print(unit.id(), Unit.Type(unit.type()), 'type')
            if unit.status() != Unit.Allocated:
                self._print(unit.id(), Unit.Status(unit.status()), 'status')
            if unit.label() is not None and unit.label() != '':
                self._print(unit.id(), unit.label(), 'label')
            for child in project.successors(unit):
                self._print(unit.id(), child.id(), 'above')
        for childClass in range(unitClass, Unit.Group):
            for unit in project.units(childClass):
                aggregate = unit.aggregate()
                if aggregate is not None:
                    self._print(unit.id(), aggregate.id(), Unit.Class(aggrgate.unitClass()))
        self._file = None

    def _print(self, source, target, tag):
        if source and tag:
            print self._writeline(doublequote(source)  + ',' + doublequote(target)  + ',' + doublequote(tag))
