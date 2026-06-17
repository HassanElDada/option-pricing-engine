#pytest for testing framework
import pytest

#numpy for math operations
import numpy as np

#we import both functions: implied volatility solves the inverse problem.
# black_scholes generates the forward prices we'll test against
from src.implied_volatility import implied_volatility
from src.black_scholes import black_scholes

# standard test parameters
S = 100
K = 100
T = 1
r = 0.05

def test_round_trip_call():
    """
    The core correctness test: price a call with a known volatility,
    then recover that volatility from the price. They should match.

    This is called a "round-trip" test - we go forward then backward
    and check we end up where we started
    """
    true_sigma = 0.2
    price = black_scholes(S,K,T,r,true_sigma,"call")

    recovered_sigma = implied_volatility(price,S,K,T,r,"call")

    assert recovered_sigma == pytest.approx(true_sigma,rel = 1e-4)

def test_round_trip_put():
    """
    Same round-trip test for put options.
    """
    true_sigma = 0.25
    price = black_scholes(S,K,T,r,true_sigma,"put")

    recovered_sigma = implied_volatility(price,S,K,T,r,"put")

    assert recovered_sigma == pytest.approx(true_sigma,rel = 1e-4)

def test_round_trip_high_volatility():
    """
    Test that the solver works correctly even at high volatility.
    Our search range goes up to 5.0 (500%), so this confirms the
    upper bound of the search range is sufficient.
    """
    true_sigma = 0.8
    price = black_scholes(S,K,T,r,true_sigma,"call")

    recovered_sigma = implied_volatility(price,S,K,T,r,"call")

    assert recovered_sigma == pytest.approx(true_sigma,rel = 1e-4)

def test_round_trip_low_volatility():
    """
    Test that solver works correctly even at very low volatility.
    """
    true_sigma = 0.05
    price = black_scholes(S,K,T,r,true_sigma,"call")

    recovered_sigma = implied_volatility(price,S,K,T,r,"call")

    assert recovered_sigma == pytest.approx(true_sigma, rel= 1e-4)

def test_round_trip_deep_in_the_money():
    """
    Test the solver on a deep in the money call 
    These options have prices close to their upper bound, so this 
    tests the solver near the edge of the valid range.
    """
    true_sigma = 0.3
    price = black_scholes(150,K,T,r,true_sigma,"call")

    recovered_sigma = implied_volatility(price,150,K,T,r,"call")

    assert recovered_sigma == pytest.approx(true_sigma, rel = 1e-4)

def test_invalid_market_price_zero():
    """
    A market price of zero or negative makes no sense - an option
    can never have zero or negative value.
    """
    with pytest.raises(ValueError):
        implied_volatility(0,S,K,T,r,"call")

def test_invalid_market_price_too_low():
    """
    A market price below the no-arbitrage lower bound should raise 
    an error - no volatility could produce this price
    """
    #for an at the money call, the lower bound is close to 0
    #but a price like 0.0001 should still be too low to be realistic
    #if it falls below the calculated lowwer bound
    discounted_K = K * np.exp(-r*T)
    lower_bound =  max(S-discounted_K,0)

    #set price below the lower bound
    too_low_price = lower_bound - 1 if lower_bound > 1 else 0.0001

    with pytest.raises(ValueError):
        implied_volatility(too_low_price,S,K,T,r, "call")
    
def test_invalid_market_price_too_high():
    """
    A market price above the no-arbitrage upper bound should raise 
    an error. For a call, the price can never exceed the stock price in S.
    """
    too_high_price = S + 10 #Above S, which is the upper bound for a call

    with pytest.raises(ValueError):
        implied_volatility(too_high_price,S,K,T,r,"call")\

def test_invalid_stock_price():
    with pytest.raises(ValueError):
        implied_volatility(10,-100,K,T,r,"call")

def test_invalid_strike_price():
    with pytest.raises(ValueError):
        implied_volatility(10,S,-100,T,r,"call")

def test_invalid_time():
    with pytest.raises(ValueError):
        implied_volatility(10,S,K,-1,r,"call")

def test_invalid_option_type():
    with pytest.raises(ValueError):
        implied_volatility(10,S,K,T,r,"banana")