#
# project: fips-munit
#

fips_begin_lib(munit)
    add_definitions(-DMUNIT_TEST_NAME_LEN=67)
    add_definitions(-DMUNIT_TEST_TIME_FORMAT="0.3f")
    fips_files(
        munit_gen.h
    )
    fips_dir(munit GROUP .)
    fips_files(
        munit.c
        munit.h
    )
fips_end_lib()
