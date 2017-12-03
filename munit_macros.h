#pragma once

#include "munit/munit.h"

#define MUNIT_TEST(Name) \
    void _munit_##Name##_fn(); \
    MunitResult _munit_##Name##_fwd(const MunitParameter params[], void* user_data) \
    { \
        (void)params; \
        (void)user_data; \
        _munit_##Name##_fn(); \
        return MUNIT_OK; \
    } \
    static const MunitTest _munit_##Name = { \
        "/" # Name, _munit_##Name##_fwd, NULL, NULL, MUNIT_TEST_OPTION_NONE, NULL \
    }; \
    void _munit_##Name##_fn()

#define MUNIT_TEST_EXTERN(Name) \
    extern MunitResult _munit_##Name##_fwd(const MunitParameter params[], void* user_data);

#define MUNIT_SUITE_EXTERN(Name) \
    extern int run_##Name##_suite(int argc, char* argv[]);
