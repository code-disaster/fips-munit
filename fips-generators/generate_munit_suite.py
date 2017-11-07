""" generate munit test suites by scanning C code """

Version = 1

import os, re, yaml
import genutil as util

tests = {}

#-------------------------------------------------------------------------------
def parseSource(srcPath):
    with open(srcPath, 'r') as f:
        src = f.read()

        re_test = re.compile('MUNIT_TEST\((.*)\)')

        matches = re_test.finditer(src)

        for match in matches:
            test_name = match.group(1)
            tests[test_name] = {
                'name': test_name
            }

#-------------------------------------------------------------------------------
def generateSource(srcPath, args):
    with open(srcPath, 'w') as f:
        f.write('// #version:{}#\n'.format(Version))
        f.write('#include "munit_gen.h"\n\n')

        for key, value in tests.items():
            f.write('MUNIT_TEST_EXTERN({});\n'.format(value['name']))

        f.write('\nstatic MunitTest _munit_tests[] = {\n')

        for key, value in tests.items():
            test_name = value['name']

            f.write('    {\n')
            f.write('        "/{}",\n'.format(test_name))
            f.write('        _munit_{}_fwd,\n'.format(test_name))
            f.write('        NULL,\n')
            f.write('        NULL,\n')
            f.write('        MUNIT_TEST_OPTION_NONE,\n')
            f.write('        NULL\n')
            f.write('    },\n')

        f.write('    {\n')
        f.write('        NULL,\n')
        f.write('        NULL,\n')
        f.write('        NULL,\n')
        f.write('        NULL,\n')
        f.write('        MUNIT_TEST_OPTION_NONE,\n')
        f.write('        NULL\n')
        f.write('    }\n')
        f.write('};\n')

        f.write('\nstatic const MunitSuite _munit_suite = {\n')
        f.write('    "/{}",\n'.format(args['suite']))
        f.write('    _munit_tests,\n')
        f.write('    NULL,\n')
        f.write('    1,\n')
        f.write('    MUNIT_TEST_OPTION_NONE\n')
        f.write('};\n')

        f.write('\nint run_{}_suite(int argc, char* argv[])\n'.format(args['suite']))
        f.write('{\n')
        f.write('    return munit_suite_main(&_munit_suite, NULL, argc, argv);\n')
        f.write('}\n')

#-------------------------------------------------------------------------------
def appendSuite(hdrPath, args):
    try:
        append = True
        with open(hdrPath, 'r') as yml:
            cfg = yaml.load(yml)
            if 'suites' in cfg:
                for suite in cfg['suites']:
                    if suite['name'] == args['suite']:
                        append = False
        if append:
            with open(hdrPath, 'a') as f:
                f.write('  - name: {}\n'.format(args['suite']))
    except:
        with open(hdrPath, 'w') as f:
            f.write('---\n')
            f.write('suites:\n')
            f.write('  - name: {}\n'.format(args['suite']))

#-------------------------------------------------------------------------------
def generate(input, out_src, out_hdr, args):
    if util.isDirty(Version, [input], [out_src]):
        parseSource(input)
        generateSource(out_src, args)
        appendSuite(out_hdr, args)
