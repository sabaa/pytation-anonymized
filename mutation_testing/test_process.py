import sys
import pytest

if __name__ == '__main__':
    args = sys.argv
    parallel_level = args[1]
    if parallel_level == '1':
        pytest.main([])
    else:
        pytest.main(["-n", parallel_level])
