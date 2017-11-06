""" generate munit test suites by scanning C code """

Version = 1

import os, re, yaml
import genutil as util

#-------------------------------------------------------------------------------
def readConfig(input):
    with open(input, 'r') as yml:
        cfg = yaml.load(yml)
        return cfg

#-------------------------------------------------------------------------------
def generateSource(srcPath, args, suites):
    with open(srcPath, 'w') as f:
        f.write('// #version:{}#\n'.format(Version))
        f.write('#include "munit_gen.h"\n\n')

        for suite in suites:
            f.write('MUNIT_SUITE_EXTERN({});\n'.format(suite))

        f.write('\nint {}_main(int argc, char* argv[])\n'.format(args['runner']))
        f.write('{\n')

        for suite in suites:
            f.write('    run_{}_suite(argc, argv);\n'.format(suite))

        f.write('    return 0;\n')
        f.write('}\n')

#-------------------------------------------------------------------------------
def generateHeader(hdrPath, args):
    with open(hdrPath, 'w') as f:
        f.write('// #version:{}#\n'.format(Version))
        f.write('#pragma once\n\n')

        f.write('extern int {}_main(int argc, char* argv[]);\n'.format(args['runner']))

#-------------------------------------------------------------------------------
def generate(input, out_src, out_hdr, args):
    if util.isDirty(Version, [input], [out_src]):
        cfg = readConfig(input)

        suites = []
        for suite in cfg['suites']:
            suites.append(suite['name'])

        suites = set(suites)

        generateSource(out_src, args, suites)
        generateHeader(out_hdr, args)
