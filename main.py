from src.black_scholes import black_scholes
from src.greeks import delta, gamma, vega, theta, rho
from src.plotting import (
    plot_price_vs_stock,
    plot_price_vs_volatility,
    plot_delta_vs_stock,
    plot_gamma_vs_stock,
    plot_vega_vs_stock,
)

#Defining our example parameters
# These represent a realistic at the money option scenario
# A stock trading at $100, with a strike price of $100 (At the money) 
# 1 year to expire, 5% risk free rate, and 20% volatility
S = 100 #stock price
K = 100 #strike price
T = 1 #time to maturity in years
r = 0.05 #risk free rate
sigma = 0.2 #volatility

def print_prices():
    """
    Calculate and print call and put prices.
    """

    call_price = black_scholes(S,K,T,r,sigma,"call")
    put_price = black_scholes(S,K,T,r,sigma,"put")

    print("=" *45)
    print("       BLACK-SCHOLES OPTION PRICING")
    print("=" *45)
    print(f"Stock Price: ${S}")
    print(f"Strike Price: ${K}")
    print(f"Time to Maturity: {T} years")
    print(f"  Risk-Free Rate (r):    {r*100:.1f}%")
    print(f"  Volatility (sigma):   {sigma*100:.1f}%")
    print("=" *45)
    print(f"  Call Price:            ${call_price:.4f}")
    print(f"  Put Price:             ${put_price:.4f}")
    print("=" *45)

def print_greeks():
    """Calculate and print all the greeks for both calls and puts"""

    print("\n" + "=" *45)
    print("              GREEKS")
    print("=" *45)
    print(f"  {'Greek':<12} {'Call':>10} {'Put':>10}")
    print("=" *45)
    
    #delta: change in option price per $1 change in stock price
    call_delta = delta(S,K,T,r,sigma,"call")
    put_delta = delta(S,K,T,r,sigma,"put")
    print(f"  {'Delta':<12} {call_delta:>10.4f} {put_delta:>10.4f}")

    #gamma: change in delta per $1 change in stock price
    #same for calls and puts
    g = gamma(S,K,T,r,sigma)
    print(f"  {'Gamma':<12} {g:>10.4f} {g:>10.4f}")

    #vega: change in option price per 1 percentage point change in volatility
    #same for calls and puts
    v = vega(S,K,T,r,sigma)
    print(f"  {'Vega':<12} {v:>10.4f} {v:>10.4f}")

    #theta: change in option price per calendar day
    call_theta = theta(S,K,T,r,sigma,"call")
    put_theta = theta(S,K,T,r,sigma,"put")
    print(f"  {'Theta':<12} {call_theta:>10.4f} {put_theta:>10.4f}")

    #rho: change in option price per 1 percentage point change in interest rates
    call_rho = rho(S,K,T,r,sigma,"call")
    put_rho = rho(S,K,T,r,sigma,"put")
    print(f"  {'Rho':<12} {call_rho:>10.4f} {put_rho:>10.4f}")

    print("=" *45)
    print("\n Units:")
    print("  Delta — per $1 move in stock price")
    print("  Gamma — per $1 move in stock price")
    print("  Vega  — per 1% change in volatility")
    print("  Theta — per calendar day")
    print("  Rho   — per 1% change in interest rate")

def run_plots():
    """Generate all sensitivity plots"""
    print("\n  Generating plots — close each window to see the next one.")
    print("  Plot 1: Option Price vs Stock Price")
    plot_price_vs_stock(K=K, T=T, r=r, sigma=sigma)

    print("  Plot 2: Option Price vs Volatility")
    plot_price_vs_volatility(S=S, K=K, T=T, r=r)

    print("  Plot 3: Delta vs Stock Price")
    plot_delta_vs_stock(K=K, T=T, r=r, sigma=sigma)

    print("  Plot 4: Gamma vs Stock Price")
    plot_gamma_vs_stock(K=K, T=T, r=r, sigma=sigma)

    print("  Plot 5: Vega vs Stock Price")
    plot_vega_vs_stock(K=K, T=T, r=r, sigma=sigma)

if __name__ == "__main__":
    print_prices()
    print_greeks()
    run_plots()