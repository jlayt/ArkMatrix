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


class GraphML(Formatter):

    def __init__(self):
        super(GraphML, self).__init__()
        self._read = False
        self._write = True

    def write(self, outfile, project, unitClass, options):
        self._file = outfile

        self._writeline('<?xml version="1.0" encoding="UTF-8"?>')

        if options['style']:
            # yEd support
            self._writeline('<graphml xmlns="http://graphml.graphdrawing.org/xmlns"')
            self._writeline('         xmlns:java="http://www.yworks.com/xml/yfiles-common/1.0/java"')
            self._writeline('         xmlns:sys="http://www.yworks.com/xml/yfiles-common/markup/primitives/2.0"')
            self._writeline('         xmlns:x="http://www.yworks.com/xml/yfiles-common/markup/2.0"')
            self._writeline('         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
            self._writeline('         xmlns:y="http://www.yworks.com/xml/graphml"')
            self._writeline('         xmlns:yed="http://www.yworks.com/xml/yed/3"')
            self._writeline(
                '         xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://www.yworks.com/xml/schema/graphml/1.1/ygraphml.xsd">')
            self._writeline('    <key for="node" id="d5" yfiles.type="nodegraphics"/>')
            self._writeline('    <key for="edge" id="d9" yfiles.type="edgegraphics"/>')
        else:
            self._writeline('<graphml xmlns="http://graphml.graphdrawing.org/xmlns"')
            self._writeline('         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
            self._writeline('         xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">')

        self._writeline('    <graph id="' + project.dataset() + '" edgedefault="directed">')

        for unit in project.units(unitClass):
            if options['style']:
                self._writeline('        <node id=' + doublequote(unit.id()) + '>')
                self._writeline('            <port name="North"/>')
                self._writeline('            <port name="South"/>')
                # yEd support
                self._writeline('            <data key="d5">')
                self._writeline('                <y:ShapeNode>')
                self._writeline('                    <y:Geometry height="' +
                                str(options['height']) + '" width="' + str(options['width']) + '"/>')
                self._writeline('                    <y:Fill hasColor="false" transparent="false"/>')
                self._writeline('                    <y:BorderStyle color="#000000" type="line" width="1.0"/>')
                self._writeline(
                    '                    <y:NodeLabel alignment="center" autoSizePolicy="content" visible="true">' + str(unit.label()) + '</y:NodeLabel>')
                self._writeline('                    <y:Shape type="rectangle"/>')
                self._writeline('                </y:ShapeNode>')
                self._writeline('            </data>')
                self._writeline('        </node>')
            else:
                self._writeline('        <node id=' + doublequote(unit.id()) + '/>')

        eid = 0
        for edge in project.matrix(unitClass).relationships():
            out = '        <edge id=' + doublequote(eid) + ' source=' + \
                doublequote(edge[0].id()) + ' target=' + doublequote(edge[1].id())
            if options['style']:
                out += ' sourceport="South" targetport="North"/>'
            else:
                out += '"/>'
            self._writeline(out)
            if options['style']:
                self._writeline('            <data key="d9">')
                self._writeline('                <y:PolyLineEdge>')
                self._writeline('                    <y:Path sx="0.0" sy="12.5" tx="0.0" ty="-12.5"/>')
                self._writeline('                    <y:LineStyle color="#000000" type="line" width="1.0"/>')
                self._writeline('                    <y:Arrows source="none" target="none"/>')
                self._writeline('                    <y:BendStyle smoothed="false"/>')
                self._writeline('                </y:PolyLineEdge>')
                self._writeline('            </data>')
            eid += 1

        self._writeline('    </graph>')
        self._writeline('</graphml>')
