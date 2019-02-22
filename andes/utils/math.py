import numpy as np
import scipy as sp
import cvxopt


# def matrix(*args, **kwargs):
#     return cvxopt.matrix(np.array(*args, **kwargs))


def mul(*args, **kwargs):
    return np.multiply(*args, **kwargs)


def exp(*args, **kwargs):
    return np.exp(*args, **kwargs)


def log(*args, **kwargs):
    return np.log(*args, **kwargs)


def altb(a, b):
    """Return a matrix of logic comparison of A<B"""
    return np.less(a, b).astype('float')


def mmax(a, b):
    """Return a matrix of maximum values in a and b element-wise"""
    return np.maximum(a, b)


def mmin(a, b):
    """Return a matrix of minimum values in a and b element-wise"""
    return np.minimum(a, b)


def agtb(a, b):
    """Return a matrix of logic comparision of A>B"""
    return np.greater(a, b).astype('float')


def aleb(a, b):
    """Return a matrix of logic comparison of A<=B"""
    return np.less_equal(a, b).astype('float')


def ageb(a, b):
    """Return a matrix of logic comparision of A>=B"""
    return np.greater_equal(a, b).astype('float')


def aeqb(a, b):
    """Return a matrix of logic comparison of A == B"""
    return np.equal(a, b).astype('float')


def aneb(a, b):
    """Return a matrix of logic comparison of A != B"""
    return np.not_equal(a, b).astype('float')


def aorb(a, b):
    """Return a matrix of logic comparison of A or B"""
    return np.logical_or(a, b).astype('float'), a.size


def aandb(a, b):
    """Return a matrix of logic comparison of A or B"""
    return np.logical_and(a, b).astype('float'), a.size


def nota(a):
    """Return a matrix of logic negative of A"""
    return np.logical_not(a).astype('float'), a.size


def polar(m, a):
    """Return complex number from polar form m*exp(1j*a)"""
    return np.multiply(m, np.exp(1j * a))


def conj(a):
    """return the conjugate of a"""
    if isinstance(a, (cvxopt.matrix, cvxopt.spmatrix)):
        return a.H.T
    elif isinstance(a, np.ndarray):
        return a.conjugate()
    elif sp.sparse.issparse(a):
        return a.conjugate()


def neg(u):
    """Return the negative of binary states u"""
    return 1 - u


def mfloor(a):
    """Return the element-wise floor value of a"""
    return np.floor(a)


def mround(a):
    """Return the element-wise round value of a"""
    return np.round(a)


def not0(a):
    """Return u if u!= 0, return 1 if u == 0"""
    return np.array(list(map(lambda x: 1 if x == 0 else x, a)))


def zeros(m, n):
    """Return a m-by-n zero-value matrix"""
    if n == 1:
        return np.zeros((m, ))
    else:
        return np.zeros((m, n))


def ones(m, n):
    """Return a m-by-n one-value matrix"""
    return np.ones((m, n))


def sign(a):
    """Return the sign of a in (1, -1, 0)"""
    return np.sign(np.array(a))


def sort(m, reverse=False):
    """Return sorted m (default: ascending order)"""
    if isinstance(m, cvxopt.matrix):
        m = list(m)
        m = sorted(m, reverse=reverse)
        return cvxopt.matrix(m)
    elif isinstance(m, list):
        m = sorted(m, reverse=reverse)
        return m


def sort_idx(m, reverse=False):
    """Return the indices of m in sorted order (default: ascending order)"""
    return sorted(range(len(m)), key=lambda k: m[k], reverse=reverse)


def index(m, val):
    """
    Return the indices of all the ``val`` in ``m``
    """
    mm = np.array(m)
    idx_tuple = np.where(mm == val)
    idx = idx_tuple[0].tolist()

    return idx


def to_number(s):
    """
    Convert a string to a number.
    If not successful, return the string without blanks
    """
    ret = s
    # try converting to float
    try:
        ret = float(s)
    except ValueError:
        ret = ret.strip('\'').strip()

    # try converting to uid
    try:
        ret = int(s)
    except ValueError:
        pass

    # try converting to boolean
    if ret == 'True':
        ret = True
    elif ret == 'False':
        ret = False
    elif ret == 'None':
        ret = None
    return ret


def sdiv(a, b):
    """Safe division: if a == b == 0, sdiv(a, b) == 1"""
    if len(a) != len(b):
        raise ValueError('Argument a and b does not have the same length')
    idx = 0
    ret = zeros(len(a), 1)
    ret = cvxopt.matrix(ret)
    for m, n in zip(a, b):
        try:
            ret[idx] = m / n
        except ZeroDivisionError:
            ret[idx] = 1
        finally:
            idx += 1
    return ret
