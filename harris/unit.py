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

import itertools

class Unit():

    # Unit.Class enum
    Context = 0
    Subgroup = 1
    Group = 2
    Landuse = 3
    Class = ['context', 'subgroup', 'group', 'landuse']

    # Unit.Type enum
    Undefined = 0
    Deposit = 1
    Fill = 2
    Cut = 3
    Masonry = 4
    Skeleton = 5
    Timber = 6
    Type = ['', 'deposit', 'fill', 'cut', 'masonry', 'skeleton', 'timber']

    # Unit.Status enum
    Allocated = 0
    Assigned = 1
    Void = 2
    Status = ['allocated', 'assigned', 'void'];

    # Counter for unique Node IDs
    _counter = itertools.count()
    # Node ID, unique over all unit types
    _nid = 0
    _siteCode = ''
    # ID, unique within unit type and site code
    _id = ''
    # Key, composed of Site Code, and ID, unique within unit type
    _key = ''
    _class = Context # Unit.Class
    _type = Undefined # Unit.Type
    _status = Allocated # Unit.Status
    _label = None
    _aggregate = None

    def __init__(self, siteCode, unitId, unitClass = Context, unitType = Undefined, unitStatus = Allocated):
        self._nid = Unit._counter.next()
        self._siteCode = siteCode
        self._id = str(unitId)
        if siteCode:
            self._key = siteCode + '_' + self._id
        else:
            self._key = self._id
        self._class = unitClass
        self._type = unitType
        self._status = unitStatus

    def __str__(self):
        return self._key

    def __hash__(self):
        return hash(self._nid)

    def __eq__(self, other):
        if not isinstance(other, Unit):
            return False
        return self._siteCode == other._siteCode and self._class == other._class and self._id == other._id

    def __lt__(self, other):
        if not isinstance(other, Unit):
            return False
        if self._siteCode != other._siteCode:
            return self._siteCode < other._siteCode
        if self._class != other._class:
            return self._class < other._class
        return self._id < other._id

    def key(self):
        return self._key

    def isValid(self):
        return self._key and self._nid

    def siteCode(self):
        return self._siteCode

    def id(self):
        return self._id

    def node(self):
        return self._nid

    def setClass(self, unitClass):
        self._class = unitClass

    def unitClass(self):
        return self._class

    def setType(self, type):
        self._type = type

    def type(self):
        return self._type

    def setStatus(self, status):
        self._status = status

    def status(self):
        return self._status

    def label(self):
        if self._label is not None and self._label != '':
            return self._label
        return self.id()

    def setLabel(self, label):
        self._label = label

    def setAggregate(self, aggregate):
        if self._class + 1 == aggregate.unitClass():
            self._aggregate = aggregate

    def aggregate(self):
        return self._aggregate
