import numpy as np


def build_regret_matrix(x):
    """

    :param x:
    :return:
    """
    r = np.zeros(x.shape)
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            r[i, j] = x[i, j] - x.min(axis=0)[j]
    return r


def build_choice_criteria_matrix(x, alpha):
    """

    :param x: (ndarray) payoff matrix
    :param alpha: (float) hurwicz balance parameter
    :return: (ndarray) choice_criteria_matrix
    """
    f_min = x.min(axis=1)
    f_med = x.mean(axis=1)
    f_max = x.max(axis=1)
    r = build_regret_matrix(x)
    a_max = r.max(axis=1)
    wald = f_max
    laplace = f_med
    savage = a_max
    hurwicz = f_max*alpha + (1-alpha)*f_min

    cc = np.array([wald, laplace, savage, hurwicz])
    cc = cc.transpose()
    return cc


def build_normalized_choice_criteria_matrix(cc):
    """

    :param cc:
    :return:
    """
    ncc = np.zeros(cc.shape)
    for i in range(cc.shape[0]):
        for j in range(cc.shape[1]):
            ncc[i, j] = (cc.max(axis=0)[j] - cc[i, j])/(cc.max(axis=0)[j] - cc.min(axis=0)[j])
    return ncc


def build_all_normalized_choice_criteria_matrix(choice_criteria):
    n_obj, n_alt, n_crit = np.shape(choice_criteria)
    normalized_choice_criteria = np.zeros([n_obj, n_alt, n_crit])
    for i in range(n_obj):
        normalized_choice_criteria[i] = build_normalized_choice_criteria_matrix(choice_criteria[i])
    normalized_choice_criteria[np.isnan(normalized_choice_criteria)] = 0
    return normalized_choice_criteria


def build_aggregated_normalized_choice_criteria_matrix(normalized_choice_criteria):
    return np.min(normalized_choice_criteria, axis=0)
