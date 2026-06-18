#numpy for creating arrays of values for plotting
#instead of calculating one price at a time, we calculate across
#hundreds of values at once
import numpy as np

#matplotlib is the standard plotting library in python
#pyplot is the submodule that gives us the tools to create figures and axes and plot lines
import matplotlib.pyplot as plt

#we import our own pricing and greeks functions that we built previously
from src.black_scholes import black_scholes
from src.greeks import delta, gamma, vega

def plot_price_vs_stock(K:float, T:float, r:float, sigma:float):
    """
    plot call and put prices across a raneg of stock prices
    This shows the classic shape of option prices, before expiry:
    -call prices raise as stock price inreases above the strike
    -put price raise as the stock falls below the strike
    -Both curves are smooth and continuous with no jumps 

    Paramteres:
    -------------
    K: strike price, the price at which the option is exercised
    T: Time to maturity in years, how long until the option expires
    r: risk-free rate, the interest rate on a riskless investment, annualized
    sigma: volatility, the standard deviation of the stock's returns, annualized
    """

    #np.linspace creates an evenly spaced array of values
    #here we create 200 values from half the strike, to double the strike price
    #200 points makes it a smooth curve
    S_range = np.linspace(K/2, K*2,200 )

    #for each stock in S_range we calculate the call and put price using our black scholes function
    call_prices = np.array([black_scholes(S, K, T, r, sigma, "call") for S in S_range])
    put_prices = np.array([black_scholes(S, K, T, r, sigma, "put") for S in S_range])

    # -----  build the plot -----
    #plt.subplots() creates a figure and an axes object
    #think of the figure as the whole canvas and the axes as the actual chart area
    #figsize = (10,6) makes the figure 10 inches wide and 6 inches tall
    fig, ax = plt.subplots(figsize=(10,6))

    #ax.plot() draws a line on the axes 
    #first argument: x (stock prices)
    #second argument: y (option prices)
    #label: what shows up in the legend
    #color: the line color
    #linewidth, how thick the line is
    ax.plot(S_range,call_prices, label = "Call Price", color = "blue", linewidth = 2)
    ax.plot(S_range, put_prices, label = "Put Price", color = "tomato", linewidth = 2)

    #axvline draws a vertical line at a specific x value, in this case the strike price
    #this makes it easier to see K on the chart
    #linestyle = "--" makes it a dashed line
    # alpha controls transparency - 0 is invisible, 1 is solid
    ax.axvline(x = K, color = "grey", linestyle = "--", linewidth = 1, label = f"Strike = {K}")

    #labels and formatting
    #set_title: title at the top of the chart
    #set_xlabel: label for the x axis
    #set_ylabel: label for the y axis
    #Legend() : shows colored labels explaining each line
    #grid() : adds faint gridlines to make values easier to read
    ax.set_title("Option price vs Stock Price", fontsize = 14)
    ax.set_xlabel("Stock Price (S)")
    ax.set_ylabel("Option Price")
    ax.legend()
    ax.grid(True, alpha = 0.3)

    #tight_layout() automatically adjusts spacing so nothing gets cut off
    #plt.show() renders and displays the plot window
    plt.tight_layout()
    plt.show()

def plot_price_vs_volatility(S:float, K:float, T:float, r:float):
    """
    Plot call and put prices across a range of volatilities

    This shows higher volatility always increases option value.

    this is because options have asymmetric payoffs:
    - If the stock moves in your favor, you profit
    - If it moves against you, the loss is limited to the premium paid 
    - So more volatility = more chance of a big move in your favor
    
    Parameters:
    S: current stock price
    K: strike price
    T: time to maturity in years
    r: risk free interest rate, annualized
    """
    #sigma_range goes from 5% volatility to 80% volatility
    #we store as decimals so 0.05 to 0.8 because that's what the formula expects
    #5% is low volatility
    #80% is very high volatility
    sigma_range = np.linspace(0.05,0.8,200)

    call_prices = np.array([black_scholes(S, K, T, r, s, "call") for s in sigma_range])
    put_prices = np.array([black_scholes(S, K, T, r, s, "put") for s in sigma_range])

    fig, ax = plt.subplots(figsize=(10,6))

    #we multiply sigma_range by 100 on the x axis to convert back to percentage 
    ax.plot(sigma_range*100, call_prices, label = "Call Price", color = "steelblue", linewidth = 2)
    ax.plot(sigma_range*100, put_prices, label = "Put Price", color = "tomato", linewidth = 2)

    ax.set_title("Option price vs Volatility", fontsize = 14)
    ax.set_xlabel("Volatility (%)")
    ax.set_ylabel("Option Price")
    ax.legend()
    ax.grid(True, alpha = 0.3)

    plt.tight_layout()
    plt.show()

def plot_delta_vs_stock(K:float, T:float, r:float, sigma:float):
    """
    Plot call and put delta across a range of stock prices.

    Delta is one of the most important Greeks, it tells you how much
    your option position moves when the stock moves.

    Key things to observe on this chart:
    -Call delta forms an S-shaped curve between 0 and 1
    -Put delta forms an S-shaped curve between -1 and 0
    -At the strike price, call delta is approximately 0.5 
    meaning roughly 50/50 chance of finishing profitable.
    -Deep in the money: delta approaches 1 meaning in the option behaves almost
    like owning the stock outright
    -Deep out of the money: delta approaches 0 meaning the option
    barely moves when the stock moves

    Parameters:
    K: strike price
    T: time to maturity in years
    r: risk-free rate
    sigma: volatility, annualized
    """
    S_range = np.linspace(K*0.5, K*2, 200)

    call_deltas = np.array([delta(S, K, T, r, sigma, "call") for S in S_range])
    put_deltas = np.array([delta(S, K, T, r, sigma, "put") for S in S_range])

    fig, ax = plt.subplots(figsize=(10,6))
    ax.plot(S_range, call_deltas, label = "Call Delta", color = "steelblue", linewidth = 2)
    ax.plot(S_range, put_deltas, label = "Put Delta", color = "tomato", linewidth = 2)

    #vertical line at the strike price for reference
    ax.axvline(x = K, color = "grey", linestyle = "--", linewidth = 1, label = f"Strike = {K}")

    #horizontal line at y = 0 as a visual baseline 
    #linewidth = 0.8, makes it thin so it doesn't dominate the chart
    ax.axhline(y = 0, color = "black", linestyle = "--", linewidth = 0.8)

    ax.set_title("Delta vs Stock Price", fontsize = 14)
    ax.set_xlabel("Stock Price (S)")
    ax.set_ylabel("Delta")
    ax.legend()
    ax.grid(True, alpha = 0.3)

    plt.tight_layout()
    plt.show()

def plot_gamma_vs_stock(K:float, T:float, r:float, sigma:float) -> None:
    """
    Plot gamma across a range of stock prices

    Gamma is the rate of change of delta with respect to the stock price
    It tells you how much your delta changes when the stock price changes

    It's the same for both calls and puts

    Key things to observe on this chart:
    -Gamma forms a bell shaped curve, peaking at the strike price
    -At the strike, delta is changing the fastest - the option is most sensitive to stock price moves here
    -Far in or out the money, gamma is near 0 - meaning delta is stable and barely changes as the stock moves
    -Traders with high gamma exposure need to rehedge their positions frequently because their delta is
    changing rapidly with every stock price move

    Parameters:
    K: strike price
    T: time to maturity in years
    r: risk-free rate
    sigma: volatility
    """
    S_range= np.linspace(K*0.5, K*2, 200)

    #gamma is the same for calls and puts so we only compute it once
    gammas = np.array([gamma(S, K, T, r, sigma) for S in S_range])

    fig,ax = plt.subplots(figsize=(10,6))

    #seagreen is a distinct color from the other option colors used in other plots
    #helps visually distinguish the gamma chart from price/delta charts
    ax.plot(S_range, gammas, label = "Gamma", color = "seagreen", linewidth = 2)
    ax.axvline(x = K, color = "grey", linestyle = "--", linewidth = 1, label = f"Strike = {K}")

    ax.set_title("Gamma vs Stock Price", fontsize = 14)
    ax.set_xlabel("Stock Price (S)")
    ax.set_ylabel("Gamma")
    ax.legend()
    ax.grid(True, alpha = 0.3)

    plt.tight_layout()
    plt.show()

def plot_vega_vs_stock(K:float, T:float, r:float, sigma:float) -> None:
    """
    Plot vega across a range of stock prices

    Vega measures how much the option price changes per 1 percentage point increase
    in volatility. It's the same for calls and puts.

    Key things to observe:
    -Vega forms a bell curve shape, peaking at the strike price
    -At the money options are most sensitive to changes in volatility, so vega is highest here
    -Deep in or out the money options have low vega, meaning high changes in volatility has low impact
    -Vega and gamma have very similar shapes, this isn't a coincidence, both peak where uncertainty about
    the outcome is highest

    Paramters:
    K: strike price
    T: time to maturity in years
    r: risk free interest rate
    sigma: volatility, annualized
    """
    S_range = np.linspace(K*0.5, K*2, 200)

    #vega is the same for calls and puts so we only compute it once
    vegas = np.array([vega(S, K, T, r, sigma) for S in S_range])

    fig,ax  = plt.subplots(figsize=(10,6))

    ax.plot(S_range, vegas, label = "Vega", color = "mediumpurple", linewidth = 2)
    ax.axvline(x = K, color = "gray", linestyle = "--", linewidth = 1, label = f"Strike = {K}")
    
    ax.set_title("Vega vs Stock Price", fontsize = 14)
    ax.set_xlabel("Stock Price (S)")

    #the y axis label reminds the reader of the units:
    #vega is expressed per 1 percentage point change in volatility
    ax.set_ylabel("Vega (per 1% change in volatility)")
    ax.legend()
    ax.grid(True, alpha = 0.3)

    plt.tight_layout()
    plt.show()

def plot_monte_carlo_convergence(S: float, K: float, T: float, r:float, sigma:float, option_type: str = "call") -> None:
    """
    Plot Monte Carlo price convergence as the number of simulations increases.

    This chart shows one of the most important properties of Monte Carlo:
    the price estimate gets closer and closer to the true Black-Scholes price
    as we run more simulations. The error shrinks proportionally to 1/sqrt(n_simulations)
    - a fundamental result in statistics.

    Key things to observe:
    -With few simulations (left side), the estimate is noisy and unreliable
    -With many simulations (right side), it converges to the true price
    -The confidence band (shaded area) shrinks as simulations increase
    -Antithetic variates converge faster than basic Monte Carlo

    Parameters:
    S: current stock price
    K: strike price
    T: time to maturity in years
    r: risk free rate
    sigma: volatility
    option_type = "call" or "put"
    """

    # we import here to avoid circular imports at the top of the file  
    from src.monte_carlo import monte_carlo_price
    from src.black_scholes import black_scholes

    #the true price from Black-Scholes - this is what Monte Carlo converges to
    bs_price = black_scholes(S,K,T,r,sigma,option_type)

    #a range of simulation counts to test
    #np.logspace gives us evenly spaced points on a log scale
    #this means we test 100,200,500,1000,2000, ..., up to 100000
    #log scale is better here because the improvement is dramatic at low counts
    # and subtle at high counts
    sim_counts = np.logspace(2,5,50).astype(int)

    mc_prices = [] #basic Monte Carlo prices
    antithetic_prices = [] #antithetic variate prices
    std_errors        = []  # standard errors for confidence band

    #run Monte Carlo for each simulation count
    for n in sim_counts:
        result = monte_carlo_price(S,K,T,r,sigma,option_type,n_simulations = n, seed = 42)
        mc_prices.append(result["price"])
        antithetic_prices.append(result["price_antithetic"])
        std_errors.append(result["std_error"])

    #convert to numpy arrays for easier match
    mc_prices = np.array(mc_prices)
    antithetic_prices = np.array(antithetic_prices)
    std_errors = np.array(std_errors)

    #discount std_errors to get confidence band
    #the true price should fall within +/- 2 standard errors 95% of the time
    upper_band = mc_prices + 2*std_errors
    lower_band = mc_prices - 2*std_errors

    #build the plot
    fig,ax = plt.subplots(figsize = (10,6))

    #basic Monte Carlo line
    ax.plot(sim_counts, mc_prices, label = "Monte Carlo", color = "steelblue", linewidth = 2)

    #antithetic variates line
    ax.plot(sim_counts, antithetic_prices, label = "Antithetic Variates", color = "mediumpurple", linewidth = 2)

    #true Black-Scholes price as a horizontal reference line
    ax.axhline(y = bs_price, color = "tomato", linestyle = "--", linewidth = 1.5,label=f"Black-Scholes = {bs_price:.4f}")

    #shaded confidence band - shows uncertainty around the basic MC estimate
    # alpha = 0.2 makes it transparent so it doesn't dominate the chart
    ax.fill_between(sim_counts, lower_band, upper_band, alpha = 0.2, color = "steelblue", label = "95% Confidence Band")

    #log scale on x axis - makes the convergence behaviour easier to see 
    ax.set_xscale("log")

    ax.set_title(f"Monte Carlo Convergence — {option_type.capitalize()} Option", fontsize=14)
    ax.set_xlabel("Number of Simulations (log scale)")
    ax.set_ylabel("Option Price")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

def plot_volatility_smile(S:float, T:float, r:float, sigma_atm:float) -> None:
    """
    Plot the implied volatility smile across different strike prices.

    In a perfect Black-Scholes world, implied volatility would be flat across all strikes
    - the model assumes constant volatility. But in real markets, out-of-the-money options trade
    at higher implied volatilies than at-the-money options, creating a smile shape.

    We simulate this by adding a realistic smile curve on top of the
    flat Black-Scholes volatility, then recovering the implied vol
    from the resulting prices. This shows what the smile looks like
    and how implied volatility varies across strikes.

    Key things to observe:
    - The smile is lowest at the money (strike = stock price)
    - It rises on both sides — higher for low strikes (puts) and
      high strikes (calls)
    - The left side (low strikes) is often steeper than the right —
      this is called volatility skew, driven by demand for crash protection

    Parameters
    ----------
    S        : current stock price
    T        : time to maturity in years
    r        : risk-free rate
    sigma_atm: the at-the-money volatility (the base volatility level)
    """
    from src.implied_volatility import implied_volatility

    #range of strike prices from 70% to 130% of the stock price
    #this covers realistic in-the-money and out-of-the-money strikes
    K_range = np.linspace(S*0.7,S*1.3,50)

    # simulate a realistic volatility smile
    # in real markets the smile is driven by supply and demand for options
    # at different strikes. We model it with a simple quadratic curve:
    #   sigma(K) = sigma_atm + skew * moneyness + smile * moneyness^2
    # where moneyness = (K - S) / S measures how far the strike is from
    # the current stock price, normalized by the stock price
    #
    # skew: negative value tilts the smile so low strikes have higher vol
    #       (this reflects real market demand for crash protection via puts)
    # smile: positive value creates the upward curve on both sides
    skew = -0.05   # left side steeper than right — realistic market behavior
    smile = 0.3  # controls how curved the smile is

    implied_vols = []

    for K in K_range:
        #moneyness: 0 means at-the-money, negative means below, positive above
        moneyness = (K-S)/S

        #true volatility for this strike - the smile-adjusted sigma
        true_sigma = sigma_atm + skew * moneyness + smile * moneyness**2

        #make sure sigma stays positive - very deep strikes could go negative
        true_sigma = max(true_sigma,0.01)

        #price the option using the smile-adjusted volatility
        price = black_scholes(S,K,T,r,true_sigma,"call")

        # now recover the implied volatility from that price
        # in a flat world this would equal true_sigma exactly
        # here it traces out the smile shape
        try:
            iv = implied_volatility(price, S, K, T, r, "call")
            implied_vols.append(iv * 100)  # convert to percentage for readability
        except ValueError:
            # skip strikes where the price falls outside arbitrage bounds
            implied_vols.append(np.nan)


    #build the plot:
    fig,ax = plt.subplots(figsize=(10,6))

    ax.plot(K_range, implied_vols,color = "steelblue", linewidth = 2, label = "Implied Volatility")

    #Vertical line at the current stock price (at-the-money point)
    ax.axvline(x=S, color = "tomato", linestyle = "--", linewidth = 1.5, label = f"ATM Strike = {S}")

    # horizontal line at the base volatility level
    ax.axhline(y=sigma_atm * 100, color="gray", linestyle="--", linewidth=1,
               label=f"ATM Vol = {sigma_atm*100:.0f}%")

    ax.set_title("Volatility Smile", fontsize=14)
    ax.set_xlabel("Strike Price (K)")
    ax.set_ylabel("Implied Volatility (%)")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()