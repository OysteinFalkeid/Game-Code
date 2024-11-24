#include <gtest/gtest.h>
#include "my_module.h"

// Test for add function
TEST(MyModuleTest, TestAdd) {
    EXPECT_EQ(add(1, 1), 2); 
    EXPECT_EQ(add(0, 0), 0);
    EXPECT_EQ(add(-1, 1), 0);
}

// Test for Fibonacci function
TEST(MyModuleTest, TestFib) {
    EXPECT_EQ(fib(0), 0);
    EXPECT_EQ(fib(1), 1);
    EXPECT_EQ(fib(5), 5);
    EXPECT_EQ(fib(10), 55);
}

// Main function for Google Test
int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}