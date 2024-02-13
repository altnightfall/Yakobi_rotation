"""Yakobi rotation function."""
from typing import Optional, Tuple
import numpy as np
import random


def yakobi_rotation(matrix: np.array, eps: float) -> Tuple[Optional[list[np.array]], str]:
    """Yakobi rotation algorithm."""
    if not isinstance(matrix, np.ndarray):
        return None, f"Wrong type!"
    if not matrix.dtype == np.float64:
        return None, f"Dtype must be float64!"
    a = np.array(matrix)
    shapes = np.shape(matrix)

    if not len(shapes) > 1:
        return None, f"It's not matrix!"
    if not all(len(vec) == len(matrix[0]) for vec in matrix):
        return None, f"It's not matrix!"
    if not all(shape == shapes[0] for shape in shapes):
        return None, f"Matrix must be square!"
    if not np.allclose(a, a.T):
        return None, f"Matrix must be symmetric"

    v = np.eye(shapes[0])

    s = 0
    for _p in range(shapes[0]):
        for _q in range(shapes[0]):
            if _p != _q:
                s += a[_p][_q] ** 2

    while True:
        el = np.array([])
        for _p in range(shapes[0]):
            for _q in range(shapes[0]):
                if _p != _q:
                    el = np.append(el, a[_p][_q])

        if np.all(el == 0):
            return [a, v], "Non diagonal elemets are all zeros!"

        while True:
            p, q = random.randint(0, max(shapes) - 1), random.randint(0, max(shapes) - 1)
            if p != q and a[p][q] != 0:
                break

        c = (a[q][q] - a[p][p]) / (2 * a[p][q])
        s -= (pow(a[p][q], 2) + pow(a[q][p], 2))

        if c >= 0:
            tg_phi = 1 / (c + np.sqrt(c ** 2 + 1))
        else:
            tg_phi = 1 / (c - np.sqrt(c ** 2 + 1))

        cos_phi = 1 / np.sqrt(1 + (pow(tg_phi, 2)))
        sin_phi = tg_phi * cos_phi

        _a = np.array(a)
        _v = np.array(v)

        _a[p][q], _a[q][p] = 0, 0
        _a[p][p] = a[p][p] - a[p][q] * tg_phi
        _a[q][q] = a[q][q] + a[p][q] * tg_phi
        for r in range(shapes[0]):
            _v[r][p] = v[r][p] * cos_phi - v[r][q] * sin_phi
            _v[r][q] = v[r][p] * sin_phi + v[r][q] * cos_phi

            if r == p or r == q:
                continue
            _a[p][r] = a[r][p] - (sin_phi * (a[r][q] + ((sin_phi / (1 + cos_phi)) * a[r][p])))
            _a[r][p] = a[r][p] - (sin_phi * (a[r][q] + ((sin_phi / (1 + cos_phi)) * a[r][p])))

            _a[q][r] = a[r][q] + (sin_phi * (a[r][p] - ((sin_phi / (1 + cos_phi)) * a[r][q])))
            _a[r][q] = a[r][q] + (sin_phi * (a[r][p] - ((sin_phi / (1 + cos_phi)) * a[r][q])))

        a = np.array(_a)
        v = np.array(_v)

        if s < eps:
            return [a, v], "S < eps!"
