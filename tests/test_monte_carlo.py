#pytest for testing framework
import pytest

#numpy for math operations in tests
import numpy as np

#Import our Monte Carlo pricer and Black-Scholes for comparison
from src.monte_carlo import monte_carlo_price
from src.black_scholes import black_scholes

#Standard test parameters
S = 100
K = 100
T = 1
r = 0.05
sigma = 0.2

def test_call_price_close_to_black_scholes():
    """
    With enough simulations, Monte Carlo should converge to the Black-Scholes price
    We use a fix seed so that the test is deterministic
    We allow a tolerance of $0.50 - since Monte Carlo is an approximation
    """
    result = monte_carlo_price(S,K,T,r,sigma, "call", n_simulations = 100000, seed = 42)
    bs_price = black_scholes(S,K,T,r,sigma, "call")
    assert abs(result["price"] -bs_price ) < 0.50

def test_put_price_close_to_black_scholes():
    """
    Same convergence test for put options.
    """
    result = monte_carlo_price(S,K,T,r,sigma,"put", n_simulations = 100000, seed = 42)
    bs_price = black_scholes(S,K,T,r,sigma, "put")
    assert abs(result["price"] - bs_price) < 0.50

def test_antithetic_price_reasonable():
    """
    The antithetic price should be within $1 of the Black-Scholes price.
    """
    result = monte_carlo_price(S, K, T, r, sigma, "call", n_simulations=100000, seed=42)
    bs_price = black_scholes(S, K, T, r, sigma, "call")
    assert abs(result["price_antithetic"] - bs_price) < 1.0

def test_price_positive():
    """
    Option prices must always be positive - you can never pay a negative 
    price for the right to do something
    """
    result = monte_carlo_price(S,K,T,r,sigma,"call", n_simulations = 10000, seed = 42)
    assert result["price"] > 0

def test_std_error_decreases_with_more_simulation():
    """
    Standard error should decrease as we run more simulations.
    This is a fundamental property of Monte Carlo - accuracy improves
    proportionally to 1/sqrt(n_simulations)
    """
    result_small = monte_carlo_price(S,K,T,r,sigma,"call", n_simulations = 1000, seed = 42)
    result_large = monte_carlo_price(S,K,T,r,sigma,"call", n_simulations = 100000, seed = 42)
    assert result_large["std_error"] < result_small["std_error"]

def test_put_call_parity():
    """
    Put-Call parity must hold under Monte-Carlo just as it does under Black-Scholes.
    This is a fundamental law of options pricing.
    Call - Put = S - K * e^(-rT)
    We allow a wider tolerance here since both sides have Monte Carlo noise.
    """
    call_result = monte_carlo_price(S, K, T, r, sigma, "call", n_simulations=100000, seed=42)
    put_result  = monte_carlo_price(S, K, T, r, sigma, "put",  n_simulations=100000, seed=42)

    left_side  = call_result["price"] - put_result["price"]
    right_side = S - K * np.exp(-r * T)

    assert abs(left_side - right_side) < 0.50

def test_higher_volatility_higher_price():
    """
    Higher volatility should always produce a higher option price.
    This is true for both Monte Carlo and Black-Scholes.
    """
    result_low_vol  = monte_carlo_price(S, K, T, r, 0.1, "call", n_simulations=100000, seed=42)
    result_high_vol = monte_carlo_price(S, K, T, r, 0.4, "call", n_simulations=100000, seed=42)

    assert result_high_vol["price"] > result_low_vol["price"]

def test_invalid_stock_price():
    with pytest.raises(ValueError):
        monte_carlo_price(-100,K,T,r,sigma,"call")

def test_invalid_strike_price():
    with pytest.raises(ValueError):
        monte_carlo_price(S, -100, T, r, sigma, "call")

def test_invalid_time():
    with pytest.raises(ValueError):
        monte_carlo_price(S, K, -1, r, sigma, "call")


def test_invalid_volatility():
    with pytest.raises(ValueError):
        monte_carlo_price(S, K, T, r, -0.2, "call")


def test_invalid_option_type():
    with pytest.raises(ValueError):
        monte_carlo_price(S, K, T, r, sigma, "banana")


def test_invalid_n_simulations():
    with pytest.raises(ValueError):
        monte_carlo_price(S, K, T, r, sigma, "call", n_simulations=-100)