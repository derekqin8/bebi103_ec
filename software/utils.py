import numpy as np
import scipy.stats
import warnings
import numba
import tqdm


def lik_log_gamma(params, y):
    """
    Computes the log likelihood of a Gamma distribution with the given parameters
    and data points.

    Args:
        params: [alpha, beta] for a Gamma distribution

    Returns:
        log likelihood
    """
    alpha, beta = params

    # constraints on alpha and beta values
    if alpha <= 0 or beta <= 0:
        return -np.inf

    return np.sum(scipy.stats.gamma.logpdf(y, a=alpha, scale=1/beta))


def mle_log_gamma(x):
    """
    Computes numerically the maximum likelihood estimator for the parameters
    of a Gamma distribution.
    """
    # use method of moments estimations for initial guesses
    alpha = np.mean(x)**2/np.var(x)
    beta = np.mean(x)/np.var(x)

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        res = scipy.optimize.minimize(
            fun=lambda params, y: -lik_log_gamma(params, y),
            x0=np.array([alpha, beta]),
            args=(x,),
            method='Powell',
            tol=1e-8
        )

    return res.x[0], res.x[1]


def exp2logpdf(x, beta1, beta2):
    if np.isclose(beta1, beta2):
        return scipy.stats.gamma.logpdf(x, a=2, scale=1/beta1)
    c = (beta1*beta2)/(beta2-beta1)
    return scipy.special.logsumexp(a=np.stack([-beta1*x, -beta2*x], axis=1), axis=1, b=np.array([c, -c]))


def lik_log_exp2(params, y):
    """
    Computes the log likelihood for the sum of 2 exponential random variables

    Args:
        params: [alpha, beta]

    Returns:
        log likelihood
    """
    beta1, beta2 = params

    if beta1 <= 0 or beta2 <= 0 or beta1 > beta2:
        return -np.inf

    return np.sum(exp2logpdf(y, beta1, beta2))


def mle_log_exp2(x):
    """
    Computes numerically the maximum likelihood estimator for the parameters
    of a Gamma distribution.
    """
    mu = np.mean(x)
    beta1, beta2 = (3/2)/mu, (3)/mu

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        res = scipy.optimize.minimize(
            fun=lambda params, y: -lik_log_exp2(params, y),
            x0=np.array([beta1, beta2]),
            args=(x,),
            method='Powell',
            tol=1e-8
        )

    if res.success:
        return res.x[0], res.x[1]
    else:
        raise RuntimeError('Convergence failed with message', res.message)


@numba.njit
def sample_gamma(alpha, beta, n, size=100000):
    """Draws size samples of length n from a Gamma distribution parameterized by alpha and beta"""
    return np.random.gamma(shape=alpha, scale=1/beta, size=(size, n))


@numba.njit
def sample_exp2(beta1, beta2, n, size=100000):
    """Draws size samples of length n from the sum of 2 exponential random variables parameterized by beta1 and beta2"""
    return np.random.exponential(scale=1/beta1, size=(size, n))+np.random.exponential(scale=1/beta2, size=(size, n))


def gamma_pbs_mle(x, B):
    """
    Generates parametric bootstrap samples using the MLE as parameters
    for a Gamma distribution.
    """
    alpha, beta = mle_log_gamma(x)
    ret = np.empty((B, 2))
    for i in tqdm.tqdm(range(B), position=0, leave=True):
        ret[i, :] = mle_log_gamma(np.random.gamma(
            shape=alpha, scale=1/beta, size=len(x)))
    return ret
