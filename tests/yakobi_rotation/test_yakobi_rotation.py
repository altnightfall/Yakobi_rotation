import numpy as np
import pytest

from yakobi_rotation import yakobi_rotation

WRONG_INPUT = [
    [],
    '',
    'ABC',
    1,
    np.array([1]),
    np.array([[1], [1]]),
    np.array([[1], [1]], dtype=np.int64),
]

MATRIXES = [
    np.array([[1, 0], [0, 1]], dtype=np.float64),
    np.array([[1, 4, 7, 10, 13],
              [4, 7, 10, 13, 16],
              [7, 10, 13, 16, 19],
              [10, 13, 16, 19, 22],
              [13, 16, 19, 22, 25]], dtype=np.float64),
    np.array([[1, 2, 3],
              [2, 3, 4],
              [3, 4, 5]], dtype=np.float64)
]

EPSILONS = [
    0.1,
    0.01,
    0.001
]


@pytest.mark.parametrize("matrix", WRONG_INPUT)
def test_wrong_input(matrix):
    response = yakobi_rotation(matrix, 0.1)
    assert response[0] is None, f"Got unexpected result"


@pytest.mark.parametrize("matrix", MATRIXES)
@pytest.mark.parametrize("eps", EPSILONS)
def test_right_input(matrix, eps):
    response = yakobi_rotation(matrix, eps)
    test = np.dot(np.dot(response[0][1], response[0][0]), response[0][1].T)
    assert np.allclose(test, matrix)
