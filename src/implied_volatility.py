#numpy for math operations
import numpy as np

# brentq is scipy's implementation of Brent's method for root-finding
from scipy.optimize import brentq

#we need our Black-Scholes pricer - implied volatility works by perfectly
#calling this function with different sigma values until the output
#matches the market price 
from src.black_scholes import black_scholes

def implied_volatility(
    market_price: float,
    S: float,
    K: float,
    T: float, 
    r: float, 
    option_type: str
) -> float:
    """
    Calculate the implied volatility given an observed market price

    This is an inverse problem of Black-Scholes: instead of
    sigma -> price, we solve price -> sigma.

    We do this by finding the sigma where:
        black_scholes(S,K,T,r,sigma, option_type) - market_price = 0

    using Brent's method, a numerical root-finding algorithm.

    Parameters:
    market_price: observed market price of the option
    S: current stock price
    K: strike price
    T: time to maturity in years
    r: risk free rate, annualized
    sigma: volatility, annualized
    option_type = "call" or "put"

    Returns:
    float
        the implied volatility, as a decimal (e.g. 0.25 as 25%)
        """
    #input validation
    if market_price <= 0:
        raise ValueError(f"Market price must be positive, got {market_price}")

    if S <= 0:
        raise ValueError(f"Stock price must be positive, got {S}")

    if K <= 0:
        raise ValueError(f"Strike price must be positive, got {K}")

    if T <= 0:
        raise ValueError(f"time to maturity must be positive, got {T}")

    if option_type not in ("call", "put"):
        raise ValueError(f"option_type must be 'call' or 'put', got '{option_type}'")

    #arbitrage bound check
    #Every option price has theoretical minimum and maximum bounds based
    #on no-arbitrage arguments, regardless of volatility.
    #                            
    # For a call: the price must be between max(S - K*e^(-rT), 0) and S
    #   - Lower bound: the call can never be worth less than its intrinsic value
    #     (what you'd get if you exercised it immediately, discounted)
    #   - Upper bound: a call can never be worth more than the stock itself,
    #     since owning the call gives you at most the right to own the stock
    #
    # For a put: the price must be between max(K*e^(-rT) - S, 0) and K*e^(-rT)
    #   - Lower bound: similarly, the intrinsic value of the put
    #   - Upper bound: a put can never be worth more than the discounted strike,
    #     since the most you could receive is K (by selling the stock at K)
    #
    # If the market price violates these bounds, no volatility (not even
    # infinity) can produce that price — it would imply an arbitrage
    # opportunity, so we raise an error.
    discounted_k = K * np.exp(-r * T)

    if option_type == "call":
        lower_bound = max(S - discounted_k, 0)
        upper_bound = S
    else:
        lower_bound = max(discounted_k - S, 0)
        upper_bound = discounted_k
    if not (lower_bound < market_price < upper_bound):
        raise ValueError(
            f"Market price {market_price} is outside the no-arbitrage bounds "
            f"[{lower_bound:.4f}, {upper_bound:.4f}] for this option. "
            f"No volatility can produce this price."
        )

    # --- define the function whose root we want to find ---
    # this is the "error" between our model price and the market price
    # we want to find the sigma that makes this error exactly zero
    def price_difference(sigma):
        model_price = black_scholes(S, K, T, r, sigma, option_type)
        return model_price - market_price

    # --- run Brent's method ---
    # we search for sigma in the range [0.001, 5.0]
    # 0.001 = 0.1% volatility (essentially no movement)
    # 5.0   = 500% volatility (extremely high, covers virtually all real cases)
    #
    # brentq requires price_difference(a) and price_difference(b) to have
    # opposite signs — this is guaranteed by our arbitrage bound check above,
    # since black_scholes approaches lower_bound as sigma -> 0
    # and approaches upper_bound as sigma -> infinity
    implied_vol = brentq(price_difference, 1e-6, 5.0)

    return implied_vol