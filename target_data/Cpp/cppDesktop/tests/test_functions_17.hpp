#include <gtest/gtest.h>

#include "unit_system.hpp"

#define EXPECT_UNIT_EQ(X, Y) EXPECT_DOUBLE_EQ((X).val(), sakurajin::unit_system::unit_cast(Y, (X).mult(), (X).off()).val())
