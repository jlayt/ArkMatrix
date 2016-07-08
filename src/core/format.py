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

import csv
from unit import Unit
from matrix import Matrix

def quote(val):
    return "'" + str(val) + "'"

def doublequote(val):
    return '"' + str(val) + '"'

class Format():

    @staticmethod
    def createFormat(fileFormat):
        if (fileFormat == 'lst'):
            return FormatLst()
        elif (fileFormat == 'graphml'):
            return FormatGraphML()
        elif (fileFormat == 'gv' or fileFormat == 'dot'):
            return FormatGv()
        elif (fileFormat == 'gxl'):
            return FormatGxl()
        elif (fileFormat == 'tgf'):
            return FormatTgf()
        elif (fileFormat == 'csv'):
            return FormatCsv()
        elif (fileFormat == 'gml'):
            return FormatGml()
        else:
            return Format()

    def read(self, infile, project):
        pass

    def write(self, project, style, sameas, width, height):
        pass


class FormatLst(Format):

    # Temp default site code
    _siteCode = ''

    def read(self, infile, project):
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
            elif unit == 'group':
                project.addGroup(unit)

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


class FormatCsv(Format):

    def read(self, infile, project):
        reader = csv.reader(infile)
        inNodes = set()
        inEdges = set()
        for record in reader:
            try:
                reln = Matrix.Above
                fromUnit = Unit(project.siteCode, record[0])
                toUnit = Unit(project.siteCode, record[1])
                if len(record) < 3 or record[2] == 'above':
                    reln = Matrix.Above
                elif record[2] == 'below':
                    reln = Matrix.Below
                elif record[2] == 'sameas':
                    reln = Matrix.SameAs
                project.addUnit(fromUnit)
                project.addUnit(toUnit)
                project.addRelationship(fromUnit, reln, toUnit)
            except:
                if record:
                    print 'Error reading row: ' + str(record)

    def write(self, project, style=False, sameas=False, width=None, height=None):
        for unit in project.units():
            for child in project.matrix.successors(unit):
                print doublequote(unit.unitId())  + ',' + doublequote(project.unit(child).unitId())


class FormatGv(Format):

    def write(self, project, style=False, sameas=False, width=None, height=None):
        print 'digraph ' + project.dataset.replace(' ', '_') + ' {'
        if style:
            project.matrix.weightForDegree()
            print '    splines=polyline' # Should be ortho but ports support not implemented
            print '    concentrate=true'
            print '    ranksep="1.0 equally"'
            print '    nodesep="2.0 equally"'
            print '    node [shape=box]'
            print '    edge [arrowhead=none headport=n tailport=s width=' + str(width) + ' height=' + str(height) + ']'

        for edge in project.matrix._strat.edges_iter(data='weight', default=1):
            out = '    ' + doublequote(project.unit(edge[0]).unitId()) + ' -> ' + doublequote(project.unit(edge[1]).unitId())
            if style:
                out += ' [weight=' + str(edge[2]) + ']'
            print out + ';'

        print '}'


class FormatGml(Format):

    def write(self, project, style=False, sameas=False, width=None, height=None):
        print 'graph ['
        print '    directed 1'

        for unit in project.units():
            print '    node ['
            print '        id ' + str(unit._nid)
            print '        label ' + doublequote(unit.unitId())
            if style:
                print '        graphics ['
                print '            type "rectangle"'
                print '            w ' + str(width)
                print '            h ' + str(height)
                print '        ]'
            print '    ]'

        eid = 0
        for edge in project.matrix._strat.edges_iter():
            print '    edge ['
            print '        id ' + str(eid)
            print '        source ' + str(project.unit(edge[0])._nid)
            print '        target ' + str(project.unit(edge[1])._nid)
            if style:
                print '        graphics ['
                print '            arrow "none"'
                print '        ]'
            print '    ]'
            eid += 1

        print ']'


class FormatGraphML(Format):

    def write(self, project, style=False, sameas=False, width=None, height=None):
        print '<?xml version="1.0" encoding="UTF-8"?>'

        if style:
            #yEd support
            print '<graphml xmlns="http://graphml.graphdrawing.org/xmlns"'
            print '         xmlns:java="http://www.yworks.com/xml/yfiles-common/1.0/java"'
            print '         xmlns:sys="http://www.yworks.com/xml/yfiles-common/markup/primitives/2.0"'
            print '         xmlns:x="http://www.yworks.com/xml/yfiles-common/markup/2.0"'
            print '         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
            print '         xmlns:y="http://www.yworks.com/xml/graphml"'
            print '         xmlns:yed="http://www.yworks.com/xml/yed/3"'
            print '         xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://www.yworks.com/xml/schema/graphml/1.1/ygraphml.xsd">'
            print '    <key for="node" id="d5" yfiles.type="nodegraphics"/>'
            print '    <key for="edge" id="d9" yfiles.type="edgegraphics"/>'
        else:
            print '<graphml xmlns="http://graphml.graphdrawing.org/xmlns"'
            print '         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
            print '         xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">'

        print '    <graph id="' + project.dataset + '" edgedefault="directed">'

        for unit in project.units():
            if style:
                print '        <node id=' + doublequote(unit.unitId()) + '>'
                print '            <port name="North"/>'
                print '            <port name="South"/>'
                #yEd support
                print '            <data key="d5">'
                print '                <y:ShapeNode>'
                print '                    <y:Geometry height="' + str(height) + '" width="' + str(width) + '"/>'
                print '                    <y:NodeLabel alignment="center" autoSizePolicy="content" visible="true">' + str(unit.unitId()) + '</y:NodeLabel>'
                print '                    <y:Shape type="rectangle"/>'
                print '                </y:ShapeNode>'
                print '            </data>'
                print '        </node>'
            else:
                print '        <node id=' + doublequote(unit.unitId()) + '/>'

        eid = 0
        for edge in project.matrix._strat.edges_iter():
            out = '        <edge id=' + doublequote(eid) + ' source=' + doublequote(project.unit(edge[0]).unitId()) + ' target=' + doublequote(project.unit(edge[1]).unitId())
            if style:
                out += ' sourceport="South" targetport="North"/>'
            else:
                out += '"/>'
            print out
            if style:
                print '            <data key="d9">'
                print '                <y:PolyLineEdge>'
                print '                    <y:Arrows source="none" target="none"/>'
                print '                    <y:BendStyle smoothed="false"/>'
                print '                </y:PolyLineEdge>'
                print '            </data>'
            eid += 1

        print '    </graph>'
        print '</graphml>'


class FormatGxl(Format):

    def write(self, project, style=False, sameas=False, width=None, height=None):
        print '<?xml version="1.0" encoding="UTF-8"?>'
        print '<!DOCTYPE gxl SYSTEM "http://www.gupro.de/GXL/gxl-1.0.dtd">'

        print '<gxl xmlns:xlink=" http://www.w3.org/1999/xlink">'

        print '    <graph id="' + project.dataset + '" edgeids="true" edgemode="directed">'

        for unit in project.units():
            print '        <node id=' + doublequote(unit.unitId()) + '/>'

        eid = 0
        for edge in project.matrix._strat.edges_iter():
            print '        <edge id=' + doublequote(eid)+ ' from="' + doublequote(project.unit(edge[0]).unitId()) + ' to=' + doublequote(project.unit(edge[0]).unitId()) + '/>'

        print '    </graph>'
        print '</gxl>'


class FormatTgf(Format):

    def write(self, project, style=False, sameas=False, width=None, height=None):
        for unit in project.units():
            print str(unit.key())  + ' ' + str(unit.unitId())
        print '#'
        for edge in project.matrix._strat.edges_iter():
            print str(project.unit(edge[0]).key())  + ' ' + str(project.unit(edge[1]).key())
