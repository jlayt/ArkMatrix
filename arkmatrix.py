#!/usr/bin/env python
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

import argparse
import os
import sys

from harris.file.format import Format
from harris.project import Project
from harris.unit import Unit


def getParser():
    parser = argparse.ArgumentParser(description='A tool to process Harris Matrix files.')
    parser.add_argument("-i", "--input", help="Choose input format, optional, defaults to infile suffix",
                        choices=['lst', 'csv'])
    parser.add_argument("-v", "--validate", help="Only validate the input file, don't process", action='store_false')
    parser.add_argument("-g", "--graph", help="Output a graph in the chosen format",
                        choices=['gv', 'dot', 'gml', 'graphml', 'gxl', 'tgf'])
    parser.add_argument("--site", help="Site Code for Matrix", default='')
    parser.add_argument("--name", help="Name for Matrix", default='')
    parser.add_argument("--nostyle", help="Don't include style formatting in graph", action='store_true')
    parser.add_argument("--same", help="Include Same-As units/relationships in graph", action='store_false')
    parser.add_argument("--orphans", help="Include orphan units in graph (format dependent)", action='store_false')
    parser.add_argument("--width", help="Width of graph node", type=float, default=50.0)
    parser.add_argument("--height", help="Height of graph node", type=float, default=25.0)
    parser.add_argument("--basename", help="Base filename for file output", default='')
    parser.add_argument("--aggregate", help="Output aggregate grouping in graph file", action='store_true')
    parser.add_argument('infile', help="Source data file", nargs='?', type=argparse.FileType('r'), default=None)
    parser.add_argument('outfile', help="Destination csv file", nargs='?', type=argparse.FileType('w'), default=None)
    return parser


def getOptions(args):
    options = vars(args)

    if args.infile and args.infile.name != '<stdin>':
        basename, suffix = os.path.splitext(args.infile.name)
        if not options['basename']:
            options['basename'] = basename
        options['input'] = suffix.strip('.').lower()
    else:
        if not options['basename']:
            if options['site']:
                options['basename'] = options['site']
            elif options['name']:
                options['basename'] = options['name']
            else:
                options['basename'] = 'matrix'
        if not options['input']:
            options['input'] = 'csv'

    if args.outfile and args.outfile.name != '<stdout>':
        basename, suffix = os.path.splitext(args.outfile.name)
        if not options['basename']:
            options['basename'] = basename
        options['outpath'] = os.path.dirname(args.outfile.name)
        options['outname'] = basename
        options['output'] = suffix.strip('.').lower()
    else:
        options['output'] = 'csv'

    options['style'] = not options['nostyle']

    if options['output']:
        options['output'] = options['output'].lower()
    else:
        options['output'] = 'none'

    if 'outname' not in options:
        if args.name and args.site:
            options['outname'] = args.site + '_' + args.name
        elif args.name:
            options['outname'] = args.name
        elif args.site:
            options['outname'] = args.site
        else:
            options['outname'] = 'matrix'

    return options


def process(infile, outfile, options):
    formatter = Format.createFormat(options['input'])
    project = formatter.read(infile, options['name'], options['site'])
    if project is None:
        sys.stdout.write('\nInvalid Input: failed to parse a valid input file\n\n')
        return
    project.resolve()

    sys.stdout.write('\nOriginal Matrix:\n\n')
    writeProjectInfo(project.info())

    if not options['orphans']:
        project.removeOrphans(Unit.Context)

    if project.isValid():
        sys.stdout.write('\n\nProcessed Matrix:\n\n')
        redundant = project.reduce()
        project.aggregate()
        writeRelationships('  Redundant Relationships: ', redundant)
        writeProjectInfo(project.info())
        for unitClass in range(Unit.Subgroup, Unit.Landuse):
            if project.matrix(unitClass).count() > 0:
                sys.stdout.write('\n\n' + Unit.Class[unitClass].title() + ' Matrix:\n\n')
                writeMatrixInfo(project.matrix(unitClass).info())
    else:
        sys.stdout.write('\n\nInvalid Matrix\n')

        for unitClass in range(Unit.Context, Unit.Landuse):
            sys.stdout.write('\nErrors in ' + Unit.Class[unitClass] + ' matrix' + '\n\n')
            duplicates = list(project.matrix(unitClass).duplicates())
            sys.stdout.write('  Cyclic Same-As Relationships: ' + str(len(duplicates)) + '\n')
            for edge in duplicates:
                sys.stdout.write('    Same-As: ' + str(list(map(str, edge))) + '\n')
            cycles = list(project.matrix(unitClass).cycles())
            sys.stdout.write('\n  Cyclic Above/Below Relationships: ' + str(len(cycles)) + '\n')
            pairs = set()
            for cycle in cycles:
                pair = (cycle[0], cycle[-1])
                pairs.add(pair)
            for pair in pairs:
                sys.stdout.write('    Cycle Pair: ' + str(list(map(str, pair))) + '\n')
        sys.stdout.write('\n')

    formatter.write(outfile, project, Unit.Context, options)
    if options['graph'] is not None:
        project.simplify()
        writeGraphFile(project, options['graph'], options)

    sys.stdout.write('\n')


def writeGraphFile(project, graph, options):
    formatter = Format.createFormat(graph)
    for unitClass in range(Unit.Context, Unit.Landuse):
        if project.matrix(unitClass).count() > 0:
            name = options['outname'] + '_' + Unit.Class[unitClass] + '.' + graph
            outfile = open(name, 'w')
            formatter.write(outfile, project, unitClass, options)
            outfile.close()
            outfile = None


def writeProjectInfo(info):
    out = '  Dataset: ' + info['dataset'] + '\n'
    out += '  Site Code: ' + info['siteCode'] + '\n'
    out += '  Total Stratigraphic Units: ' + str(info['units']) + '\n'
    out += '    - Contexts: ' + str(info['contexts']) + '\n'
    out += '    - Subgroups: ' + str(info['subgroups']) + '\n'
    out += '    - Groups: ' + str(info['groups']) + '\n'
    out += '    - Landuses: ' + str(info['landuses']) + '\n'
    out += '  Number of Orphan Contexts: ' + str(len(list(info['orphans']))) + '\n'
    if info['orphans']:
        out += '    ' + str(list(map(str, info['orphans']))) + '\n'
    if info['subgroups'] > 0:
        missing = missing = info['missing']['subgroup']
        out += '  Number of Contexts Missing Subgroup: ' + str(len(missing)) + '\n'
        if missing:
            out += '    ' + str(list(map(str, missing))) + '\n'
    if info['groups'] > 0:
        missing = info['missing']['group']
        out += '  Number of Subgroups Missing Group: ' + str(len(missing)) + '\n'
        if missing:
            out += '    ' + str(list(map(str, missing))) + '\n'
    out += '\n'
    sys.stdout.write(out)
    writeMatrixInfo(info['matrix']['context'])
    if info['subgroups'] > 0:
        writeMatrixInfo(info['matrix']['subgroup'])
    if info['groups'] > 0:
        writeMatrixInfo(info['matrix']['group'])


def writeMatrixInfo(info):
    out = '  Strat Units: ' + str(info['strat']['nodes']) + '\n'
    out += '  Strat Relationships: ' + str(info['strat']['edges']) + '\n'
    out += '  Same As Relationships: ' + str(info['same']['nodes']) + '\n'
    out += '  Contemporary Relationships: ' + str(info['contemp']['nodes']) + '\n'
    missing = info['missing']['predecessors']
    out += '  Units With No Unit Above: ' + str(len(missing)) + '\n'
    if missing:
        out += '      ' + str(list(map(str, sorted(missing)))) + '\n'
    missing = info['missing']['successors']
    out += '  Units With No Unit Below: ' + str(len(missing)) + '\n'
    if missing:
        out += '      ' + str(list(map(str, sorted(missing)))) + '\n'
    out += '  Is Valid: ' + str(info['valid']) + '\n'
    out += '  Longest Path: ' + str(info['longest']) + '\n'
    sys.stdout.write(out)


def writeRelationships(text, relationships):
    sys.stdout.write(text + str(len(relationships)) + '\n')
    for edge in relationships:
        sys.stdout.write('    ' + str(edge[0]) + ' above ' + str(edge[1]) + '\n')
    sys.stdout.write('\n')


parser = getParser()
args = parser.parse_args()
if args.infile is None:
    parser.print_help()
else:
    process(args.infile, args.outfile, getOptions(args))
