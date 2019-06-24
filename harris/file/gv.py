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


class Gv(Formatter):

    def __init__(self):
        super(Gv, self).__init__()
        self._read = False
        self._write = True

    def write(self, outfile, project, unitClass, options):
        self._file = outfile

        self._writeline('digraph ' + project.dataset().replace(' ', '_') + ' {')
        if options['style']:
            project.matrix(unitClass).weightForDegree()
            self._writeline('    splines=polyline')  # Should be ortho but ports support not implemented
            self._writeline('    concentrate=true')
            self._writeline('    ranksep="1.0 equally"')
            self._writeline('    nodesep="2.0 equally"')
            self._writeline('    node [shape=box]')
            self._writeline('    edge [arrowhead=none headport=n tailport=s width=' + str(options['width'])
                             + ' height=' + str(options['height']) + ']')

        for edge in project.matrix(unitClass).relationships(data='weight', default=1):
            out = '    ' + doublequote(edge[0].id()) + ' -> ' + doublequote(edge[1].id())
            if options['style'] and len(edge) == 3:
                out += ' [weight=' + str(edge[2]) + ']'
            self._writeline(out + ';')

        self._writeline('}')
