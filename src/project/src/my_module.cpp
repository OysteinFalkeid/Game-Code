#include "my_module.h"

float add(float a, float b) {
    return a + b;
}

int fib(int n) {

    // If n is 1 or 0, then return n, works for 0th
      // and 1st terms
    if (n <= 1)
        return n;

    // Recurrence relation to find the rest of the
      // terms
    return fib(n - 1) + fib(n - 2);
}
