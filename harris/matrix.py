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

import networkx as nx

from harris.unit import Unit

"""
A class to store, query, and manipulate a Harris Matrix.

This class is designed for speed rather than correctness, i.e. it is possible
to add cycles and self-cycles. Matrices must be validated and reduced after
new edges have been added.
"""

class Matrix():

    # Matrix.Relationship enum
    Above = 0
    Below = 1
    SameAs = 2
    ContemporaryWith = 3
    Relationship = ['above', 'below', 'sameas', 'contemporary']

    _strat = None # DiGraph()
    _same = None # Graph()
    _contemp = None # Graph()

    def __init__(self):
        self._strat = nx.DiGraph()
        self._same = nx.Graph()
        self._contemp = nx.Graph()

    def __contains__(self, unit):
        return unit in self._strat or unit in self._same or unit in self._contemp

    def info(self):
        info = {}
        info['strat'] = {}
        info['strat']['nodes'] = self._strat.number_of_nodes()
        info['strat']['edges'] = self._strat.number_of_edges()
        info['same'] = {}
        info['same']['nodes'] = self._same.number_of_nodes()
        info['same']['edges'] = self._same.number_of_edges()
        info['contemp'] = {}
        info['contemp']['nodes'] = self._contemp.number_of_nodes()
        info['contemp']['edges'] = self._contemp.number_of_edges()
        info['missing'] = {}
        info['missing']['predecessors'] = self.missingPredessors()
        info['missing']['successors'] = self.missingSuccessors()
        info['valid'] = self.isValid()
        if self.isValid() and len(self._strat) > 0:
            info['longest'] = nx.dag_longest_path_length(self._strat)
        else:
            info['longest'] = []
        return info

    def isValid(self):
        """Return True if this Matrix is valid, i.e. a Directed Acyclic Graph"""
        return self.count() == 0 or nx.is_directed_acyclic_graph(self._strat)

    def clear(self):
        """Clears the matrix"""
        self._strat.clear()
        self._same.clear()
        self._contemp.clear()

    def count(self):
        """Counts the relationships"""
        return self._strat.number_of_edges() +  self._same.number_of_edges() + self._contemp.number_of_edges()

    def addRelationship(self, fromUnit, reln, toUnit):
        """
        Add a relationship between two stratigraphic units.

        No validation is performed other than for self-cycles.

        A unit may be any hashable type such as string, number, or hashable class.
        """
        if fromUnit == toUnit:
            return False
        if reln == Matrix.Above:
            self._strat.add_edge(fromUnit, toUnit)
            return True
        elif reln == Matrix.Below:
            self._strat.add_edge(toUnit, fromUnit)
            return True
        elif reln == Matrix.SameAs:
            try:
                self._contemp.remove_edge(fromUnit, toUnit)
            except:
                pass
            self._same.add_edge(fromUnit, toUnit)
            return True
        elif reln == Matrix.ContemporaryWith:
            try:
                self._same.remove_edge(fromUnit, toUnit)
            except:
                pass
            self._contemp.add_edge(fromUnit, toUnit)
            return True
        return False

    def addRelationships(self, fromUnit, reln, toUnits):
        """
        Add a relationship between a source unit and a group of destination units.

        The destination group may be any iterable collection.
        """
        if reln == Matrix.Above:
            toUnits.insert(0, fromUnit)
            self._strat.add_star(toUnits)
        elif reln == Matrix.Below:
            for toUnit in toUnits:
                self._strat.add_edge(toUnit, fromUnit)
        elif reln == Matrix.SameAs:
            for toUnit in toUnits:
                try:
                    self._contemp.remove_edge(fromUnit, toUnit)
                except nx.NetworkXError:
                    pass
            toUnits.insert(0, fromUnit)
            self._same.add_star(toUnits)
        elif reln == Matrix.ContemporaryWith:
            for toUnit in toUnits:
                try:
                    self._same.remove_edge(fromUnit, toUnit)
                except nx.NetworkXError:
                    pass
            toUnits.insert(0, fromUnit)
            self._contemp.add_star(toUnits)

    def addRelationshipChain(self, unitsChain):
        """Add a chain of Above/Below relationships in the order of the input list."""
        self._strat.add_path(unitsChain)

    def removeUnit(self, unit):
        self._strat.remove_node(unit)
        self._same.remove_node(unit)
        self._contemp.remove_node(unit)

    def removeRelationship(self, fromUnit, reln, toUnit):
        """Remove a relationship from the Matrix if it exists."""
        if reln == Matrix.Above:
            try:
                self._strat.remove_edge(fromUnit, toUnit)
                return True
            except nx.NetworkXError:
                return False
        elif reln == Matrix.Below:
            try:
                self._strat.remove_edge(toUnit, fromUnit)
                return True
            except nx.NetworkXError:
                return False
        elif reln == Matrix.SameAs:
            try:
                self._same.remove_edge(fromUnit, toUnit)
                return True
            except nx.NetworkXError:
                return False
        elif reln == Matrix.ContemporaryWith:
            try:
                self._same.remove_edge(fromUnit, toUnit)
                return True
            except nx.NetworkXError:
                return False
        return False

    def hasRelationship(self, fromUnit, reln, toUnit):
        """Return True if a relationship type exists between two units."""
        if reln == Matrix.Above:
            return self._strat.has_edge(fromUnit, toUnit)
        elif reln == Matrix.Below:
            return self._strat.has_edge(toUnit, fromUnit)
        elif reln == Matrix.SameAs:
            return self._same.has_edge(fromUnit, toUnit)
        elif reln == Matrix.ContemporaryWith:
            return self._contemp.has_edge(fromUnit, toUnit)
        return False

    def relationships(self, reln=None):
        """Returns a list of all relationships of a certain type."""
        if reln == Matrix.SameAs:
            return self._same.edges_iter()
        if reln == Matrix.ContemporaryWith:
            return self._contemp.edges_iter()
        return self._strat.edges_iter()

    def related(self, unit, reln = None):
        """Returns a list of all units related to a unit, optionally for a certain relationship type."""
        if reln == Matrix.Above:
            return self._strat.predecessors(unit)
        elif reln == Matrix.Below:
            return self._strat.successors(unit)
        elif reln == Matrix.SameAs:
            return self._same.neighbours(unit)
        elif reln == Matrix.ContemporaryWith:
            return self._contemp.neighbours(unit)
        return sorted(self._strat.successors(unit) + self._strat.predecessors(unit) + self._same.neighbours(unit) + self._contemp.neighbours(unit))

    def predecessors(self, unit):
        """Returns a list of all units *directly* above a given unit in the matrix"""
        if unit in self._strat:
            return self._strat.predecessors(unit)
        return []

    def successors(self, unit):
        """Returns a list of all units *directly* below a given unit in the matrix"""
        if unit in self._strat:
            return self._strat.successors(unit)
        return []

    def sameAs(self, unit):
        """Returns a list of all units the same as a given unit in the matrix"""
        if unit in self._strat:
            return self._same.neighbours(unit)
        return []

    def contemporaryWith(self, unit):
        """Returns a list of all units contemporary with a given unit in the matrix"""
        return self._contemp.neighbours(unit)

    def ancestors(self, unit):
        """Returns a list of *all* units above a given unit in the matrix"""
        if unit in self._strat:
            return nx.ancestors(self._strat, unit)
        return []

    def descendents(self, unit):
        """Returns a list of *all* units below a given unit in the matrix"""
        if unit in self._strat:
            return nx.descendents(self._strat, unit)
        return []

    def hasUnit(self, unit):
        """Returns True if the matrix contains the given unit."""
        return self.__contains__(unit)

    def cycles(self):
        """Returns a list of any cycles in the matrix."""
        return nx.simple_cycles(self._strat)

    def reduceSameAs(self, project):
        """Resolve all SameAs relationships."""
        # foreach _same node, pick the lowest number
        # foreach _same node, apply all relns to lowest number
        subgraphs = nx.connected_components(self._same)
        for subgraph in subgraphs:
            subgraph = sorted(subgraph)
            unit = subgraph.pop(0)
            for sameAs in subgraph:
                self.addRelationships(self, unit, self.Below, self.predecessors(sameAs))
                self.addRelationships(self, unit, self.Above, self.descendents(sameAs))
                self.addRelationships(self, unit, self.ContemporaryWith, self.contemporaryWith(sameAs))
                project.removeUnit(sameAs)

    def reduce(self, remove=True):
        """Reduces a valid matrix by removing redundant edges. This transforms the matrix in place."""
        edges = []
        # Can only uniquely reduce the matrix if it is a DAG, i.e. no cycles or self-cycles
        if not self.isValid():
            return edges
        # Transitive reduction algorithm found on StackOverflow, algorithm originally from GraphViz tred
        # http://stackoverflow.com/questions/17078696/im-trying-to-perform-the-transitive-reduction-of-directed-graph-in-python
        for root in self._strat.nodes_iter():
            for gen1 in self._strat.successors(root):
                # Skip the direct children, look at every grandchild instead
                for gen2 in self._strat.successors(gen1):
                    # For the grandchild and all its decendents, remove any direct links back to the original unit
                    for toUnit in nx.dfs_preorder_nodes(self._strat, gen2):
                        if self._strat.has_edge(root, toUnit):
                            edges.append((root, toUnit))
                            if remove:
                                self._strat.remove_edge(root, toUnit)
        return edges

    def redundant(self):
        """Returns a list of any redundant edges without removing them."""
        return self.reduce(False)

    def missingPredessors(self):
        """Returns a list of any nodes missing a predecessor."""
        nodes = []
        for node in self._strat.nodes():
            if self._strat.in_degree(node) == 0:
                nodes.append(node)
        return nodes

    def missingSuccessors(self):
        """Returns a list of any nodes missing a successor."""
        nodes = []
        for node in self._strat.nodes():
            if self._strat.out_degree(node) == 0:
                nodes.append(node)
        return nodes

    def weight(self, fromUnit, toUnit):
        if fromUnit in self._strat and toUnit in self._strat:
            return self._strat[fromUnit][toUnit]['weight']

    def weightForDegree(self):
        for edge in self._strat.edges_iter():
            weight = 1
            if self._strat.out_degree(edge[0]) == 1:
                weight += 2
            if self._strat.in_degree(edge[1]) == 1:
                weight += 2
            self._strat[edge[0]][edge[1]]['weight'] = weight
