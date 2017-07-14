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

class Gxl(Formatter):

    def __init__(self):
        self._read = False
        self._write = True

    def write(self, project, options):
        print '<?xml version="1.0" encoding="UTF-8"?>'
        print '<!DOCTYPE gxl SYSTEM "http://www.gupro.de/GXL/gxl-1.0.dtd">'

        print '<gxl xmlns:xlink=" http://www.w3.org/1999/xlink">'

        print '    <graph id="' + project.dataset() + '" edgeids="true" edgemode="directed">'

        for unit in project.units():
            print '        <node id=' + doublequote(unit.id()) + '/>'

        eid = 0
        for edge in project.matrix(Unit.Context).relationships():
            frm = edge[0]
            to = edge[1]
            print '        <edge id=' + doublequote(eid)+ ' from="' + doublequote(edge[0].id()) + ' to=' + doublequote(edge[1].id()) + '/>'
            eid += 1

        print '    </graph>'
        print '</gxl>'
