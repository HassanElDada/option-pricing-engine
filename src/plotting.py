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
    ax.plot(S_range,call_prices, Label = "Call Price", color = "blue", linewidth = 2)
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
    plt.tight_Layout()
    plt.show()