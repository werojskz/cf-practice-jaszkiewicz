"""European calloption:Black-ScholesformulaandMonteCarloestimator."""
import numpy as np
from scipy.stats import norm

def bs_call(S0,K,r,sigma,T):
    """Black-ScholespriceofaEuropeancall."""
    d1=(np.log(S0/K)+(r+sigma**2/2)*T)/(sigma*np.sqrt(T))
    d2=d1-sigma*np.sqrt(T)
    return S0*norm.cdf(d1)-K*np.exp(-r*T)*norm.cdf(d2)


def mc_call(S0,K,r,sigma,T,n,rng):
    """MonteCarlopriceofaEuropeancallwithnpaths:(price,standarderror)."""
    Z=rng.standard_normal(n)
    ST=S0 *np.exp((r-sigma**2/2)*T+sigma*np.sqrt(T)*Z)
    payoff=np.exp(-r*T)*np.maximum(ST-K,0.0)
    return payoff.mean(),payoff.std(ddof=1)/np.sqrt(n)