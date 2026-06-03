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