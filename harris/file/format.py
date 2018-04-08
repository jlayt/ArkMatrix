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

from harris.file.csvfile import Csv
from harris.file.gml import Gml
from harris.file.graphml import GraphML
from harris.file.gv import Gv
from harris.file.gxl import Gxl
from harris.file.lst import Lst
from harris.file.tgf import Tgf


class Format():

    @staticmethod
    def createFormat(suffix):
        if (suffix == 'lst'):
            return Lst()
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
