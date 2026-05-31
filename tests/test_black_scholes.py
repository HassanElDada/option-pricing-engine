#pytest is the testing framework
#pytest.approx lets us compare floating numbers with a tolerance
import pytest

#we import it for complex math and for the normal distribution
import numpy as np

#we import the function we want to test
from src.black_scholes import black_scholes

#now we define standard values for our tests
S = 100 #stock price
K = 100 #strike price
T = 1 #time to maturity in years
r = 0.05 #risk free rate
sigma = 0.2 #volatility

def test_call_price():
    """
    test that our call price matches the known black scholes reference value
    10.4506 is the well known result for these paramters
    """
    price = black_scholes(S, K, T, r, sigma, "call")
    #will crash with assertion error if they aren't equal
    assert price == pytest.approx(10.4506, rel=1e-4)

def test_put_price():
    """
    test that our put price matches the known black scholes reference value
    """
    price = black_scholes(S, K, T, r, sigma, "put")
    assert price == pytest.approx(5.5735, rel=1e-3)

def test_put_call_parity():
    """
    put call parity is a fundamental law of options pricing
    Call - put = S - K * exp(-r*T) 
    
    if our model is correct, then this should hold for any parameters
    """

    call = black_scholes(S, K, T, r, sigma, "call")
    put = black_scholes(S, K, T, r, sigma, "put")

    left_side = call - put
    right_side = S - K * np.exp(-r*T)

    assert left_side == pytest.approx(right_side, rel=1e-6)

def test_call_price_deep_in_the_money():
    """
    A deep in the money call (stock price much higher than strike)
    should be worth approximately S - K * exp(-r*T) almost its intrinsic value
    with S much greater than K, the option will most certainly be exercised, so the time value is minimal
    """
    price = black_scholes(200, 100, T, r, sigma, "call")
    intrinsic = 200 - 100 * np.exp(-r*T)
    assert price == pytest.approx(intrinsic, rel = 1e-2)


def test_call_price_deep_out_the_money():
    """
    A deep out of the money put (stock price much lower than strike)
    should be worth nearly 0, since it's very unlikely to be exercised, the time value is minimal
    """
    price = black_scholes(50, 100, T, r, sigma, "call")
    assert price == pytest.approx(0, abs = 1e-2)

def test_invalid_stock_price():
    """
    A negative or a zero stock price makes no financial sense
    our function should raise a ValueError immediately
    """
    with pytest.raises(ValueError):
        black_scholes(-100, K, T, r, sigma, "call")

def test_invalid_strike_price():
    with pytest.raises(ValueError):
        black_scholes(S, -100, T, r, sigma, "call")

def test_invalid_time():
    with pytest.raises(ValueError):
        black_scholes(S, K, -1, r, sigma, "call")

def test_invalid_volatility():
    with pytest.raises(ValueError):
        black_scholes(S, K, T, r, -0.2, "call")

def test_invalid_option_type():
    with pytest.raises(ValueError):
        black_scholes(S, K, T, r, sigma, "invalid_option_type")

