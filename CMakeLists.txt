#
# project: fips-munit
#

fips_begin_lib(munit)

    # using some slightly modified settings
    add_definitions(-DMUNIT_TEST_NAME_LEN=67)
    add_definitions(-DMUNIT_TEST_TIME_FORMAT="0.3f")

    fips_files(
        munit_macros.h
    )

    fips_dir(munit GROUP .)
    fips_files(
        munit.c
        munit.h
    )

    if (FIPS_CLANG OR FIPS_GCC)
        set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wno-missing-field-initializers -Wno-unused-function")
    endif()

fips_end_lib()
