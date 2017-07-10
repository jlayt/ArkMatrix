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

from harris.unit import Unit
from harris.matrix import Matrix
from harris.utilities import *

class Gv():

    def write(self, project, options):
        print 'digraph ' + project.dataset.replace(' ', '_') + ' {'
        if options['style']:
            project.matrix.weightForDegree()
            print '    splines=polyline' # Should be ortho but ports support not implemented
            print '    concentrate=true'
            print '    ranksep="1.0 equally"'
            print '    nodesep="2.0 equally"'
            print '    node [shape=box]'
            print '    edge [arrowhead=none headport=n tailport=s width=' + str(options['width']) + ' height=' + str(options['height']) + ']'

        for edge in project.matrix._strat.edges_iter(data='weight', default=1):
            out = '    ' + doublequote(project.unit(edge[0]).unitId()) + ' -> ' + doublequote(project.unit(edge[1]).unitId())
            if options['style']:
                out += ' [weight=' + str(edge[2]) + ']'
            print out + ';'

        print '}'
