fips-munit
==========

A fipsified version of **µunit** (https://github.com/nemequ/munit), a unit testing framework for C.

fips build system: https://github.com/floooh/fips

## Basic use

To use µunit directly, just include `<munit/munit.h>`. Refer to the [µunit documentation](https://nemequ.github.io/munit/) for more information.

## Code generation

fips-munit defines a small set of CMake and C macros for easier integration of unit tests into your code base.

In the following example, assume that we want to run some unit tests defined in `my_code.c`, in a command line app `my_app`, with a test runner we call `my_tests`.

> Note: *work in progress*! Doesn't use some of µunits advanced features yet, like parameterized tests. Also, API might still change.

### Source code

First, implement unit tests in some of your source files.

`my_code.c`:
```
/* also includes <munit/munit.h> */
#include <munit_gen.h>

static int some_func()
{
    /* ... test-worthy code ... */
    return ...;
}

/* define some test */
MUNIT_TEST(some_func_returns_one)
{
    munit_assert_int(some_func(), == , 1);
}
```

Then, you just need to include and call the to-be-generated test runner somewhere in your application code.

`my_app.c`:
```
/* auto-generated test runner (see below) */
#include "my_tests_runner.h"

/* entry function to run all tests */
int main(int argc, char* argv[])
{
    return my_tests_main(argc, argv);
}
```

### CMake

```
fips_begin_app(my_app cmdline)

  fips_files(my_code.c my_app.c)

  # define our test runner
  fips_munit_begin(my_tests)
    # files to parse for generating tests
    fips_munit_files(my_code.c)
  fips_munit_end()

  # link static library
  fips_deps(munit)

fips_end_app()

# optional: run my_app as post-build step
fips_munit_run(my_app)
```

> `fips_munit_begin(my_tests)`

This defines a new test runner, `my_tests`. Must be called inside a `fips_begin_app()/fips_end_app()` block, and must be followed by `fips_munit_end()`.

> `fips_munit_files([files]...)`

Adds a set of source files to the test runner. These source files are scanned for `MUNIT_TEST()` macros to auto-generate unit tests from. Each of these source files defines one µunit test suite.

> `fips_munit_end()`

This macro finalizes the test runner started with `fips_munit_begin()`. It auto-generates a `my_tests_main()` function accessible through `my_tests_runner.h`, which by itself runs all known test suites.

> `fips_munit_run(my_app[, args...])`

This macro is just for convenience, and must be called *after* `fips_end_app()`. It adds a custom command to run `my_app` as a post-build step. You need to make sure yourself that `my_app`'s main() function then calls `my_tests_main()`.

### Output

If used as described above, CMake will generate the following files:

- `my_code_suite.c` with a µunit test suite which includes all tests found in `my_code.c`
- `my_tests.yml` which is used internally to list all test suites, for generating the test runner
- `my_tests_runner.c` and `my_tests_runner.h` with entry code to run all suites, one after another.

The post-build step output will look like this:

```
  Running test suite with seed 0x15534978...
  /my_code/some_func_returns_one      [ OK    ] [ 0.000 / 0.000 CPU ]
  1 of 1 (100%) tests successful, 0 (0%) test skipped.
```
