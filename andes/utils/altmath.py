"""Create a wrapper for numpy array and scipy sparse to
provide CVXOPT matrix interfaces"""

import numpy as np

from numpy import ndarray
from numpy import sin, cos, tan, power, multiply, divide, concatenate  # NOQA

import scipy as sp
from scipy.sparse import csr_matrix, diags, bmat, lil_matrix  # NOQA
from scipy import linalg  # NOQA

import cvxopt

from functools import reduce

import builtins


def round(number, dec=0):
    if isinstance(number, ndarray):
        return np.round(number, dec)
    return builtins.round(number, dec)


def spmatrix(x, I, J, size=None, tc='d', nodense=False):
    """Construct a `scipy.csr_matrix` using the cvxopt.spmatrix interface
    """

    # if isinstance(x, (int, float)):
    #     if isinstance(I, list):
    #     x = [x] * len(I)

    ret = csr_matrix((x, (I, J)), shape=size)

    if size[1] == 1 and ret.nnz > 0 and (not nodense):
        return ret.toarray().reshape((-1))
    else:
        return ret


def cvxspmatrix(x):
    """Convert a scipy sparse matrix to cvxopt.spmatrix
    """
    x = x.tocoo()
    return cvxopt.spmatrix(x.data, x.row, x.col, x.shape)


def cvxmatrix(x):
    """Convert a numpy array to cvxopt.matrix
    """
    return cvxopt.matrix(x)


def matrix(x, size=None, tc='d', dtype=None, copy=True, order='K', subok=False, ndmin=0,
           twodim=False):
    """Construct a `numpy.ndarray` using the cvxopt,matrix interface

    :param twodim: force to 2-D array even if constructed from a 1-D array-like
    :type twodim: bool
    """
    assert tc == 'd', "Only real matrices are supported"

    # convert csr_matrix to dense array
    if isinstance(x, csr_matrix):
        return x.toarray()

    ret = np.array(x, dtype=dtype, copy=copy, order=order, subok=subok, ndmin=ndmin)

    if ret.ndim == 1 and twodim:
        ret = ret.reshape((-1, 1))

    return ret


def spdiag(x, shape=None, format=None, dtype=None):
    """Construct a sparse diagonal csr_matrix using the cvxopt.spdiag interface
    """
    if x.ndim == 2 and x.shape[1] == 1:
        x = x.flat

    return diags(x, offsets=0, shape=shape, format=format, dtype=dtype)


def sparse(x, tc='d',):
    """Wrapper for sparse matrix using cvxopt.sparse interface"""
    assert tc == 'd', "only real matrices are supported"
    return csr_matrix(x)


def mul(*args):
    """Wrapper for csr_matrix.multiply"""
    if isinstance(args[0], np.ndarray):
        return +reduce(np.multiply, args)
    elif isinstance(args[0], cvxopt.spmatrix):
        return +reduce(cvxopt.mul, args)
    elif isinstance(args[0], cvxopt.matrix):
        return +reduce(cvxopt.mul, args)
    else:
        return sp.multiply(*args)


def div(*args):
    """Wrapper for numpy matrix division"""
    return np.divide(*args)


def zeros(*args, dtype=float, order='C', twodim=False):
    """Wrapper for numpy.zeros"""
    # if y == 1 and not twodim:
    #     return np.zeros(x, dtype=dtype, order=order)

    return np.zeros(*args, dtype=dtype, order=order)


def ones(*args, dtype=float, order='C', twodim=False):
    """Wrapper for numpy.ones"""
    # 1-D array
    # if y == 1 and not twodim:
    #     return np.ones(x, dtype=dtype, order=order)

    # 2-D array by default
    return np.ones(*args, dtype=dtype, order=order)


def uniform(size):
    """Wrapper for numpy.random.uniform using cvxopt.uniform interface"""
    return np.random.uniform(low=0.0, high=1.0, size=size)


def polar(a, b):
    """Return complex number from polar form

    :param a: length of the vector
    :param b: polar angle of the vector

    :type: a: array-like
    :type: b: array-like
    """
    if isinstance(a, (int, float)) and isinstance(b, (float, int)):
        a = np.array([a])
        b = np.array([b])
    elif isinstance(a, (int, float)):
        a = a * ones(*b.shape)
    elif isinstance(b, (int, float)):
        b = b * ones(*a.shape)

    return mul(a, cos(b)) + 1j * mul(a, sin(b))


def exp(*args, **kwargs):
    return matrix(np.exp(*args, **kwargs))


def conj(x):
    """Return the complex conjugate, element-wise"""
    return np.conj(x)


def agtb(a, b):
    """Return the truth value of a > b
    """
    return np.greater(a, b)


def ageb(a, b):
    """Return the truth value of a >= b
    """
    return np.greater_equal(a, b)


def aleb(a, b):
    """Return the truth value of a <= b
    """
    return np.less_equal(a, b)


def altb(a, b):
    """Return the truth value of a < b
    """
    return np.less(a, b)


def log(x):
    """Natural logarithm, element-wise
    """
    return np.log(x)


def tolist(x):
    """Convert a 2-D, single column array to a flat list
    """
    assert x.ndim == 2 and x.shape[1] == 1
    return x.reshape((-1,)).tolist()


def vertcat(*args):
    """Vertical concatenation of 2-D single column arrays
    """
    # for item in args:
    #     assert item.shape[1] == 1
    return concatenate(args, axis=0)
