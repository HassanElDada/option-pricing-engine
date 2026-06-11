#numpy for fast array operations and random number generation
import numpy as np

def monte_carlo_price(
    S:float, 
    K:float,
    T:float,
    r:float,
    sigma:float,
    option_type:str,
    n_simulations:int = 10000,
    seed: int = None
) -> dict:
    """
    Price a European option using Monte Carlo simulation.

    Instead of using a closed-form formula like Black-Scholes, we simulate 
    thousands of possible future stock prices and averages the payoffs.

    Parameters:
    S: Current stock price
    K: Strike price
    T: Time to maturity in years
    r: Risk-free interest rate (annualized)
    sigma: Volatility (annualized)
    option_type: "call" or "put"
    n_simulations: Number of Monte Carlo simulations to run (more = more accurate but slower)
    seed: Random seed for reproducibility. If set, results are always the same. Useful for testing. If none, results may vary each run.

    Returns:
    dict with keys:
    price: The Monte Carlo estimated option price 
    std_error: Standard error of the estimate (measures uncertainty) 
    price_antithetic: price using antithetic variates (more accurate)
    """

    # --- Input validation ---
    if S <= 0:
        raise ValueError(f"Stock price must be positive, got {S}")
    if K <= 0:
        raise ValueError(f"Strike price must be positive, got {K}")
    if T <= 0:
        raise ValueError(f"Time to maturity must be positive, got {T}")
    if sigma <= 0:
        raise ValueError(f"Volatility must be positive, got {sigma}")
    if option_type not in ("call", "put"):
        raise ValueError(f"Option type must be 'call' or 'put', got {option_type}")
    if n_simulations <= 0:
        raise ValueError(f"Number of simulations must be positive, got {n_simulations}")
    
    # Set random seed if provided
    # this makes results reproducible - same seed always gives some random numbers
    if seed is not None:
        np.random.seed(seed)

    # Step 1: Simulate future stock prices
    #draw n_simulation random numbers from the standard normal distribution
    #each Z represents one possible random outcome for the stock
    Z = np.random.standard_normal(n_simulations)

    #apply the Geometric Brownian Motion formula to get Future stock prices 
    # S(T) = S * exp((r - sigma^2/2) * T + sigma * sqrt(T) * Z))
#
    # (r - sigma^2/2) * T  : the expected drift of the stock over time
    #                         we subtract sigma^2/2 due to Ito's lemma — the same
    #                         correction we saw in the Black-Scholes d1 formula
    # sigma * sqrt(T) * Z  : the random component — how much the stock deviates
    #                         from its expected path due to volatility
    ST = S * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)


    # Step 2: Calculate payoffs at maturity
    # for each simulated future price, what would the option pay out
    # np.maximum(x,0) is equivalent to max(x,0) but works on arrays
    if option_type == "call":
        #call pays out if stock ends above strike price: Max(S(T) - K,0)
        payoffs = np.maximum(ST - K, 0)
    else:
        #put pays out if stock ends below strike price: Max(K - S(T),0)
        payoffs = np.maximum(K - ST, 0)

    # Step 3: Discount and average
    # the present value of the average payoff
    # np.exp(-r * T) discounts future cash back to today
    price = np.exp(-r * T) * np.mean(payoffs)

    #standard error measures how uncertain out estimate is
    #lower standard error = more reliable price estimate
    #it shrinks as we run more simulations (proportional to 1/sqrt(n_simulations))
    std_error =np.std(payoffs) / np.sqrt(n_simulations)

    # Antithetic variates: 
    # for every Z we used, also use -Z
    #this gives us a second set of simulated stock prices that are negatively
    #correlated with the first set, which reduces variance significantly
    Z_anti = -Z # flip the sign of every random number 
    ST_anti = S * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z_anti)

    if option_type == "call":
        payoffs_anti = np.maximum(ST_anti - K, 0)
    else:
        payoffs_anti = np.maximum(K - ST_anti, 0)

    # average the original and antithetic payoffs together
    # each pair (payoff, payoff_anti) gives one combined estimate
    combined_payoffs = (payoffs + payoffs_anti) / 2
    price_antithetic = np.exp(-r * T) * np.mean(combined_payoffs)

    return {
        "price": round(price,4),
        "std_error": round(std_error,4),
        "price_antithetic": round(price_antithetic,4)
    }
