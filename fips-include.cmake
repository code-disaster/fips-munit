macro(fips_munit_begin name)
    set(CurSuites)
    set(CurSuitesRunner ${name})
endmacro()

#-------------------------------------------------------------------------------
# fips_munit_files(files...)
#
# Add .c/.cpp files to parse and auto-generate unit test suites.
#
macro(fips_munit_files files)
    foreach (cur_file ${ARGV})
        get_filename_component(f_name ${cur_file} NAME_WE)
        fips_generate(
            FROM ${cur_file}
            TYPE generate_munit_suite
            SOURCE ${f_name}_suite.c
            HEADER ${CurSuitesRunner}.yml
            OUT_OF_SOURCE
            ARGS "{ suite: ${f_name} }"
        )
        list(APPEND CurSuites ${cur_file})
    endforeach()
endmacro()

macro(fips_munit_end)
    list(REMOVE_DUPLICATES CurSuites)
    set(suites "")
    foreach (cur_file ${CurSuites})
        set(suites "${suites} ${cur_file},")
    endforeach()
    fips_generate(
        FROM ${CMAKE_CURRENT_BINARY_DIR}/${CurSuitesRunner}.yml
        TYPE generate_munit_suite_runner
        SOURCE ${CurSuitesRunner}_runner.c
        HEADER ${CurSuitesRunner}_runner.h
        OUT_OF_SOURCE
        ARGS "{ runner: ${CurSuitesRunner} }"
    )
    add_custom_command(
        TARGET ${CurTargetName}
        POST_BUILD
        COMMAND ${CurTargetName}
    )
endmacro()

macro(fips_munit_run)
    add_custom_command(
        TARGET ${CurTargetName}
        POST_BUILD
        COMMAND ${CurTargetName} ${ARGN}
    )
endmacro()
