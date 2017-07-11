#!/usr/bin/env python
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

import os, sys, argparse

from harris.project import Project
from harris.unit import Unit
from harris.file.format import Format

def parseArguments():
    parser = argparse.ArgumentParser(description='A tool to process Harris Matrix files.')
    parser.add_argument("-i", "--input", help="Choose input format, optional, defaults to infile suffix", choices=['lst', 'csv'])
    parser.add_argument("-o", "--output", help="Choose output format, optional, defaults to outfile suffix", choices=['none', 'gv', 'dot', 'gml', 'graphml', 'gxl', 'tgf', 'csv'])
    parser.add_argument("-r", "--reduce", help="Apply a transitive reduction to the input graph", action='store_true')
    parser.add_argument("-a", "--aggregate", help="Generate aggregate Matrices", action='store_true')
    parser.add_argument("-s", "--style", help="Include basic style formatting in output", action='store_true')
    parser.add_argument("--all", help="Apply full options to processing, i.e. reduce, aggregate, style", action='store_true')
    parser.add_argument("--site", help="Site Code for Matrix", default='')
    parser.add_argument("--name", help="Name for Matrix", default='')
    parser.add_argument("--sameas", help="Include Same-As relationships in output", action='store_true')
    parser.add_argument("--orphans", help="Include orphan units in output (format dependent)", action='store_true')
    parser.add_argument("--width", help="Width of node if --style is set", type=float, default=50.0)
    parser.add_argument("--height", help="Height of node if --style is set", type=float, default=25.0)
    parser.add_argument('infile', help="Source data file", nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', help="Destination data file", nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    return parser.parse_args()

def options(args):
    options = vars(args)

    if not options['input'] and args.infile.name != '<stdin>':
        basename, suffix = os.path.splitext(args.infile.name)
        options['input'] = suffix.strip('.')
    if not options['input']:
        options['input'] = 'csv'
    options['input'] = options['input'].lower()

    if not options['output'] and args.outfile.name != '<stdout>':
        basename, suffix = os.path.splitext(args.outfile.name)
        options['output'] = suffix.strip('.')
        options['outpath'] = os.path.dirname(args.outfile.name)
        options['outname'] = basename
    if not options['output']:
        options['output'] = 'none'
    options['output'] = options['output'].lower()

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

    sys.stdout.write('\nOriginal Matrix:\n\n')
    writeProjectInfo(project.info())

    if not options['orphans']:
        project.removeOrphans(Unit.Context)

    if not project.isValid():
        sys.stdout.write('\n\nInvalid Matrix\n\n')
        for matrix in project.matrices():
            for cycle in matrix.cycles():
                sys.stdout.write('Cycle: ' + str(cycle) + '\n')
        sys.stdout.write('\n')
        return

    sys.stdout.write('\n\nProcessed Matrix:\n\n')
    if options['aggregate']:
        redundant = project.aggregate()
        writeRelationships(redundant)
        writeProjectInfo(project.info())
        for unitClass in range(Unit.Subgroup, Unit.Landuse):
            if project.matrix(unitClass).count() > 0:
                sys.stdout.write('\n\n' + Unit.Class[unitClass].title() + ' Matrix:\n\n')
                writeMatrixInfo(project.matrix(unitClass).info())
    elif options['reduce']:
        redundant = project.reduce()
        writeRelationships(redundant)
        writeProjectInfo(project.info())
    else:
        redundant = project.redundant()
        writeRelationships(redundant)

    if outfile or options['output'] != 'none':
        old_stdout = sys.stdout
        formatter = Format.createFormat(options['output'])
        for unitClass in range(Unit.Context, Unit.Landuse):
            print Unit.Class[unitClass] + ' ' + str(project.matrix(unitClass).count())
            if project.matrix(unitClass).count() > 0:
                print str(outfile)
                if not outfile:
                    name = options['outpath'] + options['outname'] + '_' + Unit.Class[unitClass] + '.' + options['output']
                    print name
                    outfile = open(name, 'w')
                    print(outfile)
                sys.stdout = outfile
                formatter.write(project, unitClass, options)
            outfile.close()
        outfile.close()
        sys.stdout = old_stdout

    sys.stdout.write('\n')

def writeProjectInfo(info):
    out = '  Dataset: ' + info['dataset'] + '\n'
    out += '  Site Code: ' + info['siteCode'] + '\n'
    out += '  Total Stratigraphic Units: ' + str(info['units']) + '\n'
    out += '    - Contexts: ' + str(info['contexts']) + '\n'
    out += '    - Subgroups: ' + str(info['subgroups']) + '\n'
    out += '    - Groups: ' + str(info['groups']) + '\n'
    out += '    - Landuses: ' + str(info['landuses']) + '\n'
    out += '  Number of Orphan Contexts: ' + str(len(info['orphans'])) + '\n'
    if info['orphans']:
        out += '    ' + str(info['orphans']) + '\n'
    if info['subgroups'] > 0:
        missing = missing = info['missing']['subgroup']
        out += '  Number of Contexts Missing Subgroup: ' + str(len(missing)) + '\n'
        if missing:
            out += '    ' + str(map(str, missing)) + '\n'
    if info['groups'] > 0:
        missing = info['missing']['group']
        out += '  Number of Subgroups Missing Group: ' + str(len(missing)) + '\n'
        if missing:
            out += '    ' + str(map(str, missing)) + '\n'
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
    out += '  Missing Predecessors: ' + str(len(missing)) + '\n'
    if missing:
        out += '      ' + str(map(str, sorted(missing))) + '\n'
    missing = info['missing']['successors']
    out += '  Missing Successors: ' + str(len(missing)) + '\n'
    if missing:
        out += '      ' + str(map(str, sorted(missing))) + '\n'
    out += '  Is Valid: ' + str(info['valid']) + '\n'
    out += '  Longest Path: ' + str(info['longest']) + '\n'
    sys.stdout.write(out)

def writeRelationships(relationships):
    sys.stdout.write('  Redundant Relationships: ' + str(len(relationships)) + '\n')
    for edge in relationships:
        sys.stdout.write('    ' + str(edge[0]) + ' above ' + str(edge[1]) + '\n')
    sys.stdout.write('\n')

args = parseArguments()
process(args.infile, args.outfile, options(args))
