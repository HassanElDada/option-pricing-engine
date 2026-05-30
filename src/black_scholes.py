import numpy as np #for complex math
from scipy.stats import norm #for cdf norm

def black_scholes(S: float, K: float, T: float , r:float, sigma: float, option_type: str) -> float:
    """
    Calculate the price of a European call or put option using the Black-Scholes formula.

    S: float
        current stock price
    K: float
        strike price
    T: float
        time to maturity in years
    r: float
        risk free interest rate, annualized
    sigma: float
        Volatility of the underlying stock, annualized
    option_type: str
        "call" for call option, "put" for put option
    
    Returns:
    float: the theoretical price of the option
    """

    #start off with input validation
    if S<= 0:
        raise ValueError(f"Stock price must be positive, got {S}")
    if K <= 0:
        raise ValueError(f"Strike price must be positive, got {K}")
    if T <= 0:
        raise ValueError(f"Time to maturity must be positive, got {T}")
    if sigma <= 0:
        raise ValueError(f"Volatility must be positive, got {sigma}")
    if option_type not in ["call", "put"]:
        raise ValueError(f"Option type must be 'call' or 'put', got {option_type}")
    
    #compute d1 
    #break it down into parts
    #part 1: ln(S/K) this how far the current price is from the strike price,
    # if its positive then its good, it means its in the money, this is possible if S>K for call options, and S<K for put options
    #
    #part 2: r + (sigma^2)/2 this is the risk free rate plus half the variance
    #the expected stock growth adjusted for volatility
    #
    #part 3: sigma *sqrt(T) this is the volatility adjusted for time, the more time to mature, then more time to be volatile

    #d1 is the standardized distance to the strike price, adjusted for expected growth and volatility (first )

    d1 = (np.log(S/K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

    #d2 is shifted down by one volatility over time
    d2 = d1 - (sigma * np.sqrt(T))


    #Now to compute the actual option price

    if(option_type == "call"):
        price =  (S*norm.cdf(d1)) - (K * np.exp(-r*T) * norm.cdf(d2))
    else:
        price = (K * np.exp(-r*T) * norm.cdf(-d2)) - (S*norm.cdf(-d1))
    return price