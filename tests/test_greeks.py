#pytest is the testing framework
import pytest

# we import all the greek functions we want to test
from src.greeks import delta, gamma, vega, theta,rho

#standard test inputs used across all tests
S = 100 #stock price
K = 100 #strike price
T = 1 #time to maturity in years
r = 0.05 #risk free rate
sigma = 0.2 #volatility

def test_call_delta_range():
    """
    call delta must always be between 0 and 1
    it represents a probability so it can never go outside this range
    """
    d = delta(S, K, T, r, sigma, "call")
    assert 0 < d < 1

def test_put_delta_range():
    """ 
    put delta must always be between -1 and 0
    it is negative because puts gain value when the stock falls
    """
    d = delta(S, K, T, r, sigma, "put")
    assert -1 < d < 0

def test_call_delta_value():
    """
    for our standard at the money inputs, call delta should be ~0.6368
    """
    d = delta(S, K, T, r, sigma, "call")
    assert d == pytest.approx(0.6368, rel=1e-3)

def test_put_call_delta_relationship():
    """
    call delta minus put delta must always equal exactly 1
    this is a direct consequence of put call parity
    """
    call_delta = delta(S, K, T, r, sigma, "call")
    put_delta = delta(S, K, T, r, sigma, "put")
    assert call_delta - put_delta == pytest.approx(1.0, rel=1e-6)

def test_gamma_positive():
    """
    gamma is always positive for both calls and puts
    since it represents the rate of change of delta which always increases
    as ths stock price rises
    """
    g = gamma(S, K, T, r, sigma)
    assert g > 0

def test_gamma_value():
    """
    for our standard at the money inputs, gamma should be ~0.0188
    """
    g = gamma(S, K, T, r, sigma)
    assert g == pytest.approx(0.0188, rel=1e-2)

def test_vega_positive():
    """
    vega is always positive - higher volatility always means higher option price
    because it increases the probability of the option finishing in the money
    """
    v = vega(S, K, T, r, sigma)
    assert v > 0

def test_vega_value():
    """
    for our standard at the money inputs, vega should be ~0.3752
    """
    v = vega(S, K, T, r, sigma)
    assert v == pytest.approx(0.3752, rel=1e-3)

def test_call_theta_negative():
    """
    theta is almost always negative - options lose value as time passes
    this is called time decay
    """
    t = theta(S, K, T, r, sigma, "call")
    assert t < 0

def test_call_rho_positive():
    """
    Call rho is always positive - higher interest rates increase the call option price
    because they reduce the present value of the strike price
    """
    r_val = rho(S, K, T, r, sigma, "call")
    assert r_val > 0

def test_put_rho_negative():
    """
    put rho is always negative - higher interest rates decrease the put option price
    """
    r_val = rho(S, K, T, r, sigma, "put")
    assert r_val < 0