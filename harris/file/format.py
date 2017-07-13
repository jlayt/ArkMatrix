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

from harris.file.csvfile import Csv
from harris.file.gml import Gml
from harris.file.graphml import GraphML
from harris.file.gv import Gv
from harris.file.gxl import Gxl
from harris.file.lst import Lst
from harris.file.tgf import Tgf

class Format():

    _file = None

    @staticmethod
    def createFormat(suffix):
        if (suffix == 'lst'):
            return Lst(outfile)
        elif (suffix == 'csv'):
            return Csv()
        elif (suffix == 'graphml'):
            return GraphML()
        elif (suffix == 'gv' or suffix == 'dot'):
            return Gv()
        elif (suffix == 'gxl'):
            return Gxl()
        elif (suffix == 'tgf'):
            return Tgf()
        elif (suffix == 'gml'):
            return Gml()
        return None

    def _writeline(line):
        self._file.write(str(line) + '\n')
