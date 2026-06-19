# Options Pricing and Volatility Analytics Engine

A Black-Scholes options pricing engine built in Python, featuring European call and put pricing, all five Greeks, Monte Carlo simulation, implied volatility solving, and a full test suite.

---

## Why This Project Matters

Options pricing is at the core of quantitative finance. Every major bank, hedge fund, and trading firm prices derivatives daily using models rooted in Black-Scholes. Understanding and implementing these models from scratch — including the Greeks, Monte Carlo simulation, and implied volatility — demonstrates the mathematical and software engineering foundations expected in quant roles.

---

## Features

- European call and put pricing using the Black-Scholes formula
- All five Greeks: Delta, Gamma, Vega, Theta, Rho
- Monte Carlo simulation using Geometric Brownian Motion with antithetic variance reduction
- Implied volatility solver using Brent's method
- Volatility smile visualization
- Input validation with clear error messages
- 46 passing unit tests using pytest
- 7 sensitivity and analysis plots using Matplotlib
- Clean, well-commented, professional Python code

---

## Black-Scholes Formula

The Black-Scholes model prices European options using five inputs:

| Input | Symbol | Description |
|---|---|---|
| Stock Price | S | Current market price of the underlying stock |
| Strike Price | K | Price at which the option can be exercised |
| Time to Maturity | T | Time until expiry, in years |
| Risk-Free Rate | r | Annualized continuously compounded risk-free rate |
| Volatility | sigma | Annualized standard deviation of stock returns |

**Intermediate values:**

```
d1 = [ln(S/K) + (r + sigma^2/2) * T] / [sigma * sqrt(T)]
d2 = d1 - sigma * sqrt(T)
```

**Option prices:**

```
Call = S * N(d1) - K * e^(-rT) * N(d2)
Put  = K * e^(-rT) * N(-d2) - S * N(-d1)
```

Where N(x) is the cumulative standard normal distribution function.

---

## The Greeks

Greeks measure how sensitive the option price is to changes in market conditions.

| Greek | Measures | Call | Put |
|---|---|---|---|
| Delta | Change in option price per $1 move in stock | 0 to 1 | -1 to 0 |
| Gamma | Change in Delta per $1 move in stock | Always positive | Always positive |
| Vega | Change in option price per 1% move in volatility | Always positive | Always positive |
| Theta | Change in option price per calendar day | Usually negative | Usually negative |
| Rho | Change in option price per 1% move in interest rates | Positive | Negative |

---

## Project Structure

```
option-pricing-engine/
|
|-- src/
|   |-- __init__.py
|   |-- black_scholes.py        # Black-Scholes pricing formula
|   |-- greeks.py               # Delta, Gamma, Vega, Theta, Rho
|   |-- monte_carlo.py          # Monte Carlo pricer with antithetic variates
|   |-- implied_volatility.py   # Implied volatility solver using Brent's method
|   |-- plotting.py             # All sensitivity and analysis plots
|
|-- tests/
|   |-- test_black_scholes.py
|   |-- test_greeks.py
|   |-- test_monte_carlo.py
|   |-- test_implied_volatility.py
|
|-- notebooks/
|-- conftest.py
|-- main.py
|-- requirements.txt
|-- README.md
```

---

## Installation

**1. Clone the repository**
```bash
git clone https://github.com/HassanElDada/option-pricing-engine.git
cd option-pricing-engine
```

**2. Create and activate a virtual environment**
```bash
# Mac/Linux
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

---

## Running the Demo

```bash
python main.py
```

This will print option prices, Greeks, Monte Carlo comparison, and implied volatility table to the terminal, then generate 7 plots.

---

## Running the Tests

```bash
pytest tests/ -v
```

46 tests should pass.

---

## Example Output

```
=============================================
       BLACK-SCHOLES OPTION PRICING
=============================================
Stock Price: $100
Strike Price: $100
Time to Maturity: 1 years
  Risk-Free Rate (r):    5.0%
  Volatility (sigma):   20.0%
=============================================
  Call Price:            $10.4506
  Put Price:             $5.5735
=============================================

=============================================
              GREEKS
=============================================
  Greek            Call        Put
=============================================
  Delta          0.6368    -0.3632
  Gamma          0.0188     0.0188
  Vega           0.3752     0.3752
  Theta         -0.0176    -0.0045
  Rho            0.5323    -0.4189
=============================================

=============================================
       MONTE CARLO vs BLACK-SCHOLES
=============================================
                       Call        Put
---------------------------------------------
  Black-Scholes      10.4506     5.5735
  Monte Carlo        10.4739     5.6045
  Antithetic         10.4611     5.5812
  Std Error           0.0490     0.0454
=============================================
  Simulations: 100,000

=============================================
         IMPLIED VOLATILITY SOLVER
=============================================
  Strike    Market Price    Implied Vol
---------------------------------------------
  80            0.0265        20.00%
  90            1.8692        20.00%
  100          10.4506        20.00%
  110          25.6898        20.00%
  120          44.5234        20.00%
=============================================
```

---

## Roadmap

| Status | Feature |
|---|---|
| Completed | Black-Scholes pricing, Greeks, tests, plots |
| Completed | Monte Carlo pricing with antithetic variance reduction |
| Completed | Implied volatility solver and volatility smile |
| Coming Soon | Interactive Streamlit dashboard |
| Coming Soon | Volatility surface, exotic options |

---

## Dependencies

| Library | Version | Purpose |
|---|---|---|
| NumPy | >=1.24.0 | Mathematical operations |
| SciPy | >=1.10.0 | Normal distribution and Brent's method |
| Matplotlib | >=3.7.0 | Sensitivity and analysis plots |
| pytest | >=7.4.0 | Unit testing |

---

## Author

Hassan El Dada — [GitHub](https://github.com/HassanElDada) | [LinkedIn](https://www.linkedin.com/in/hassan-el-dada-b88190266/)