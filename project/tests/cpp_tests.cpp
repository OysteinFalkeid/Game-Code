#include <iostream>
#include "my_module.h"


int main() {
    std::cout << "Running C++ Tests\n";



    float Test_add = add(1,1);
    if (Test_add == 3) {
        std::cout << "Test passed: add(2) == 2\n";
    } else {
        std::cout << "Test failed: add(2) != 2\n";
        return 1; // Non-zero return indicates failure
    }

    //Check Fibonacci
    int test_fib = fib(5);
    if (test_fib == 5) {
        std::cout << "Test passed: fib(5) == 5\n";
    } else {
        std::cout << "Test failed: fib(5) != 5\n";
        return 1; // Non-zero return indicates failure
    }

    return 0; // Success

    
}
