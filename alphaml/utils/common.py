# -*- encoding: utf-8 -*-

import os
import warnings

__all__ = [
    'check_pid',
    'warn_if_not_float'
]


def warn_if_not_float(X, estimator='This algorithm'):
    """Warning utility function to check that data type is floating point.
    Returns True if a warning was raised (i.e. the input is not float) and
    False otherwise, for easier input validation.
    """
    if not isinstance(estimator, str):
        estimator = estimator.__class__.__name__
    if X.dtype.kind != 'f':
        warnings.warn("%s assumes floating point values as input, "
                      "got %s" % (estimator, X.dtype))
        return True
    return False


def check_pid(pid):
    """Check For the existence of a unix pid."""
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True


def check_true(p):
    if p in ("True", "true", 1, True):
        return True
    return False


def check_false(p):
    if p in ("False", "false", 0, False):
        return True
    return False


def check_none(p):
    if p in ("None", "none", None):
        return True
    return False


def check_for_bool(p):
    if check_false(p):
        return False
    elif check_true(p):
        return True
    else:
        raise ValueError("%s is not a bool" % str(p))

def get_max_index(num_list, topk=3):
    num_dict = {}
    for i in range(len(num_list)):
        num_dict[i] = num_list[i]
    res_list = sorted(num_dict.items(), key=lambda e: e[1])
    max_num_index = [x[0] for x in res_list[::-1][:topk]]
    return max_num_index

def get_most(num_list):
    temp = 0
    for i in num_list:
        if num_list.count(i) > temp:
            max_num = i
            temp = num_list.count(i)
    return max_num