""" generate munit test suites by scanning C code """

Version = 5

import os, re, yaml
import genutil as util

#-------------------------------------------------------------------------------
def readConfig(input):
    with open(input, 'r') as yml:
        cfg = yaml.load(yml)
        return cfg

#-------------------------------------------------------------------------------
def generateSource(srcPath, args):
    with open(srcPath, 'w') as f:
        f.write('// #version:{}#\n'.format(Version))
        f.write('#include "munit_macros.h"\n')
        f.write('#include <stdio.h>\n\n')

        for suite in args['suites']:
            f.write('MUNIT_SUITE_EXTERN({});\n'.format(suite))

        f.write('\nint {}_main(int argc, char* argv[])\n'.format(args['runner']))
        f.write('{\n')

        for suite in args['suites']:
            f.write('    printf("--------------------------------------------------------------------------------------------------\\n");\n')
            f.write('    printf("-- test suite: \'{}\'\\n");\n'.format(suite))
            f.write('    printf("--------------------------------------------------------------------------------------------------\\n");\n')
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
    if util.isDirty(Version, [input], [out_src, out_hdr]):
        generateSource(out_src, args)
        generateHeader(out_hdr, args)
