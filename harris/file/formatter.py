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


class Formatter(object):

    def __init__(self):
        self._read = False
        self._write = False
        self._file = None

    def canRead(self):
        return self._read

    def canWrite(self):
        return self._write

    def read(self, infile, dataset='', siteCode=''):
        return

    def write(self, outfile, project, unitClass, options):
        return

    def _writeline(self, line):
        if self._file:
            self._file.write(str(line) + '\n')

    def _unit(self, project, unitId, unitClass):
        if project.hasUnit(unitId, unitClass):
            return project.unit(unitId, unitClass)
        unit = Unit(project.siteCode(), unitId, unitClass)
        project.addUnit(unit)
        return unit
