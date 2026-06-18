from src.black_scholes import black_scholes
from src.monte_carlo import monte_carlo_price
from src.plotting import plot_monte_carlo_convergence
from src.greeks import delta, gamma, vega, theta, rho
from src.plotting import (
    plot_price_vs_stock,
    plot_price_vs_volatility,
    plot_delta_vs_stock,
    plot_gamma_vs_stock,
    plot_vega_vs_stock,
)
from src.implied_volatility import implied_volatility
from src.plotting import plot_volatility_smile

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

def print_monte_carlo_comparison():
    """
    Run Monte Carlo pricing and compare it against Black-Scholes
    """
    print("\n" + "=" * 45)
    print("       MONTE CARLO vs BLACK-SCHOLES")
    print("=" * 45)

    #exact Black-Scholes prices for comparison
    bs_call = black_scholes(S,K,T,r,sigma,"call")
    bs_put = black_scholes(S,K,T,r,sigma,"put")

    #monte carlo prices with 100,000 simulations
    mc_call = monte_carlo_price(S,K,T,r,sigma,"call", n_simulations = 100000, seed = 42)
    mc_put = monte_carlo_price(S,K,T,r,sigma,"put", n_simulations = 100000, seed = 42)
    print(f"  {'':<20} {'Call':>10} {'Put':>10}")
    print("-" * 45)
    print(f"  {'Black-Scholes':<20} {bs_call:>10.4f} {bs_put:>10.4f}")
    print(f"  {'Monte Carlo':<20} {mc_call['price']:>10.4f} {mc_put['price']:>10.4f}")
    print(f"  {'Antithetic':<20} {mc_call['price_antithetic']:>10.4f} {mc_put['price_antithetic']:>10.4f}")
    print(f"  {'Std Error':<20} {mc_call['std_error']:>10.4f} {mc_put['std_error']:>10.4f}")
    print("=" * 45)
    print(f"\n  Simulations: 100,000")
    print(f"  As simulations increase, Monte Carlo converges to Black-Scholes.")

def print_implied_volatility():
    """
    Demonstrate the implied volatility solver across different strikes.
    """
    print("\n" + "=" * 45)
    print("         IMPLIED VOLATILITY SOLVER")
    print("=" * 45)
    print(f"  {'Strike':<10} {'Market Price':>12} {'Implied Vol':>12}")
    print("-" * 45)

    #compute implied volatility for a range of strikes
    #we use sigma = 0.2 to generate the market price
    strikes = [80,90,100,110,120]
    for K_val  in strikes:
        price = black_scholes(S,K_val, T,r,sigma, "call")
        iv = implied_volatility(price,S,K_val, T,r,"call")
        print(f"  {K_val:<10} {price:>12.4f} {iv*100:>11.2f}%")

    print("=" * 45)
    print("\n  All implied vols recover the original sigma (0.20)")
    print("  since we used Black-Scholes prices as input.")
    print("  In real markets, implied vols vary across strikes")
    print("  — this is the volatility smile.")

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
    print("  Plot 6: Monte Carlo Convergence")
    plot_monte_carlo_convergence(S=S, K=K, T=T, r=r, sigma=sigma, option_type="call")

    print("  Plot 7: Volatility Smile")
    plot_volatility_smile(S=S, T=T, r=r, sigma_atm=sigma)



if __name__ == "__main__":
    print_prices()
    print_greeks()
    print_monte_carlo_comparison()
    print_implied_volatility()
    run_plots()