#for complicated math we use numpy
import numpy as np

#for normal cdf we use scipy
from scipy.stats import norm

def compute_d1_d2(S:float, K:float, T:float, r:float, sigma:float):
    """
    compute d1 and d2 the two intermediate values
    this is a helper function, so that we don't need to repeat the same code in all the greeks functions
    """
    d1 = (np.log(S / K) + (r + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return d1, d2


def delta(S:float, K:float, T:float, r:float, sigma:float, option_type:str) -> float:
    """
    calculate delta - the rate of change of option price with respect to the stock price

    example: if stock price increases by $1, then by how much does the option price change

    call delta: N(d1) where N is Normal cdf
    put delta: N(d1) - 1 
    """

    d1, _ = compute_d1_d2(S, K, T, r, sigma)

    if(option_type == "call"):
        return norm.cdf(d1)
    else:
        return norm.cdf(d1) - 1


def gamma(S:float, K:float, T:float, r:float, sigma:float) -> float:
    """
    Calculate gamma - the rate of change of delta with respect to the stock price 

    example: if stock price increases by $1, then by how much does the delta change

    High gamma means delta changes rapidly, usually high near expiry and strike price

    gamma: N(d1) / (S * sigma * sqrt(T)) where N is the normal pdf
    """
    d1, _ = compute_d1_d2(S,K,T,r,sigma)

    return norm.pdf(d1) / (S * sigma * np.sqrt(T))

def vega(S:float, K:float, T:float, r:float, sigma:float) -> float:
    """
    Calculate vega - the rate of change of option price with respect to volatility

    example: if volatility increases by 1 percentage point, then by how much does the option price change

    vega is the same for both puts and calls
    vega is always positive, higher volatility means higher option price

    we divide by 100 to convert from percentage points to decimal
    """
    d1, _ = compute_d1_d2(S,K,T,r,sigma)

    return S * norm.pdf(d1) * np.sqrt(T) / 100

def theta(S:float, K:float, T:float, r:float, sigma:float, option_type:str) -> float:
    """
    Calculate theta - the rate of change of option price with respect to time to maturity 

    example: as one calendar day passes, then by how much does the option price change

    theta is almost always negative, since the option loses value as time passes, this is called time decay
    we divide by 365 to convert from annualized to daily
    """
    d1,d2 = compute_d1_d2(S,K,T,r,sigma)
    if(option_type == "call"):
        return (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) - r * K * np.exp(-r*T) * norm.cdf(d2)) / 365
    else:
        return (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) + r * K * np.exp(-r*T) * norm.cdf(-d2)) / 365
    
def rho(S:float, K:float, T:float, r:float, sigma:float, option_type:str) -> float:
    """
    Calculate rho - the rate of change of option price with respect to risk free interest rate

    example: if risk free interest rate increases by 1 percentage point, then by how much does the option price change

    Call Rho is positive, higher interest rates mean higher call option prices
    Put Rho is negative, higher interest rates mean lower put option prices
    
    we divide by 100 to express Rho per 1 percentage point change in interest rates
    """
    _,d2 = compute_d1_d2(S,K,T,r,sigma)

    if (option_type == "call"):
        return K * T * np.exp(-r*T) * norm.cdf(d2) / 100
    else:
        return -K * T * np.exp(-r*T) * norm.cdf(-d2) / 100
            
