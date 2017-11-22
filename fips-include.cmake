#-------------------------------------------------------------------------------
# fips_munit_begin(name)
#
# Prepares to setup a new test runner.
#
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
        list(APPEND CurSuites ${f_name})
        fips_generate(
            FROM ${cur_file}
            TYPE generate_munit_suite
            SOURCE ${f_name}_suite.c
            HEADER ${CurSuitesRunner}.yml
            OUT_OF_SOURCE
            ARGS "{ suite: ${f_name} }"
        )
    endforeach()
endmacro()

#-------------------------------------------------------------------------------
# fips_munit_end()
#
# Auto-generates test runner with all suites found by fips_munit_files().
#
macro(fips_munit_end)
    string(REPLACE ";" "," suites "${CurSuites}")
    fips_generate(
        FROM ${CMAKE_CURRENT_BINARY_DIR}/${CurSuitesRunner}.yml
        TYPE generate_munit_suite_runner
        SOURCE ${CurSuitesRunner}_runner.c
        HEADER ${CurSuitesRunner}_runner.h
        OUT_OF_SOURCE
        ARGS "{ suites: [ ${suites} ], runner: ${CurSuitesRunner} }"
    )
endmacro()

#-------------------------------------------------------------------------------
# fips_munit_run(target, [args...])
#
# Launch test runner as a post-build custom command.
#
macro(fips_munit_run target)
    add_custom_command(
        TARGET ${target}
        POST_BUILD
        COMMAND ${target} ${ARGN}
    )
endmacro()
