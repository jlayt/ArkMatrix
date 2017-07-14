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

from harris.file.formatter import Formatter
from harris.unit import Unit
from harris.matrix import Matrix
from harris.utilities import *

class GraphML(Formatter):

    def __init__(self):
        self._read = False
        self._write = True

    def write(self, project, options):
        print '<?xml version="1.0" encoding="UTF-8"?>'

        if options['style']:
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

        print '    <graph id="' + project.dataset() + '" edgedefault="directed">'

        for unit in project.units():
            if options['style']:
                print '        <node id=' + doublequote(unit.id()) + '>'
                print '            <port name="North"/>'
                print '            <port name="South"/>'
                #yEd support
                print '            <data key="d5">'
                print '                <y:ShapeNode>'
                print '                    <y:Geometry height="' + str(options['height']) + '" width="' + str(options['width']) + '"/>'
                print '                    <y:NodeLabel alignment="center" autoSizePolicy="content" visible="true">' + str(unit.id()) + '</y:NodeLabel>'
                print '                    <y:Shape type="rectangle"/>'
                print '                </y:ShapeNode>'
                print '            </data>'
                print '        </node>'
            else:
                print '        <node id=' + doublequote(unit.id()) + '/>'

        eid = 0
        for edge in project.matrix(Unit.Context).relationships():
            out = '        <edge id=' + doublequote(eid) + ' source=' + doublequote(edge[0].id()) + ' target=' + doublequote(edge[1].id())
            if options['style']:
                out += ' sourceport="South" targetport="North"/>'
            else:
                out += '"/>'
            print out
            if options['style']:
                print '            <data key="d9">'
                print '                <y:PolyLineEdge>'
                print '                    <y:Arrows source="none" target="none"/>'
                print '                    <y:BendStyle smoothed="false"/>'
                print '                </y:PolyLineEdge>'
                print '            </data>'
            eid += 1

        print '    </graph>'
        print '</graphml>'
