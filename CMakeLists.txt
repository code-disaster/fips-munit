#
# project: fips-munit
#

fips_begin_lib(munit)
    fips_dir(munit GROUP .)
    fips_files(
        munit.c
        munit.h
    )
fips_end_lib()
