import pytest

import sys

# adding Folder_2 to the system path
sys.path.append('D:/Server/Master/Python_cxx/project/build/python/Release')

from my_python_module import *

def test_add():
    sum = add(1,1)
    assert sum == 3.0, f"the add function returns {sum} but shold return 2"
    print('Test passed')
    
def test_fib():
    fibonachi = fib(5)
    assert fibonachi == 5, f"the add function returns {fibonachi} but shold return 5"