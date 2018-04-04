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

from harris.file.formatter import Formatter
from harris.unit import Unit


class Tgf(Formatter):

    def __init__(self):
        super(Tgf, self).__init__()
        self._read = False
        self._write = True

    def write(self, project, options):
        for unit in project.units(Unit.Context):
            print str(unit.key()) + ' ' + str(unit.id())
        print '#'
        for unit in project.units(Unit.Context):
            for successor in project.matrix(Unit.Context).successors():
                print str(unit.key()) + ' ' + str(successor.key())
