
# Add Python tests (e.g., using pytest)
add_custom_target(pytest ALL COMMAND pytest ${CMAKE_CURRENT_SOURCE_DIR})

# Add C++ tests
add_executable(cpp_test cpp_tests.cpp)
target_link_libraries(cpp_test PRIVATE my_core)

# Register the test with CTest
add_test(NAME cpp_test COMMAND cpp_test)

add_custom_target(run_tests
    COMMAND ${CMAKE_CTEST_COMMAND} --output-on-failure -C $<CONFIG>
    COMMENT "Running all tests after build"
)




