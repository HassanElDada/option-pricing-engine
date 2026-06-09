# Options Pricing and Volatility Analytics Engine

A Black-Scholes options pricing engine built in Python, featuring European call and put pricing, all five Greeks, sensitivity analysis plots, and a full test suite.

---

## Why This Project Matters

Options pricing is at the core of quantitative finance. Every major bank, hedge fund, and trading firm prices derivatives daily using models rooted in Black-Scholes. Understanding and implementing these models from scratch — including the Greeks and their sensitivities — demonstrates the mathematical and software engineering foundations expected in quant roles.

---

## Features

- European call and put pricing using the Black-Scholes formula
- All five Greeks: Delta, Gamma, Vega, Theta, Rho
- Input validation with clear error messages
- 21 passing unit tests using pytest
- Sensitivity plots using Matplotlib
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
| Volatility | σ | Annualized standard deviation of stock returns |

**Intermediate values:**

```
d1 = [ln(S/K) + (r + σ²/2) * T] / [σ * √T]
d2 = d1 - σ * √T
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
│
├── src/
│   ├── __init__.py
│   ├── black_scholes.py   
│   ├── greeks.py          
│   └── plotting.py        
│
├── tests/
│   ├── test_black_scholes.py
│   └── test_greeks.py
│
├── notebooks/
│
├── conftest.py
├── main.py
├── requirements.txt
└── README.md
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

This will print option prices and all Greeks to the terminal, then generate five sensitivity plots.

---

## Running the Tests

```bash
pytest tests/ -v
```

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

  Units:
  Delta — per $1 move in stock price
  Gamma — per $1 move in stock price
  Vega  — per 1% change in volatility
  Theta — per calendar day
  Rho   — per 1% change in interest rate
```

---

## Roadmap

| Week | Feature |
|---|---|
| ✅ Week 1 | Black-Scholes pricing, Greeks, tests, plots |
| 🔜 Week 2 | Monte Carlo option pricing with variance reduction |
| 🔜 Week 3 | Implied volatility solver using Brent's method |
| 🔜 Week 4 | Interactive Streamlit dashboard |
| 🔜 Later | Volatility smile and surface, exotic options |

---

## Dependencies

| Library | Version | Purpose |
|---|---|---|
| NumPy | >=1.24.0 | Mathematical operations |
| SciPy | >=1.10.0 | Normal distribution functions |
| Matplotlib | >=3.7.0 | Sensitivity plots |
| pytest | >=7.4.0 | Unit testing |

---

## Author

Hassan El Dada — [GitHub](https://github.com/HassanElDada) | [LinkedIn](https://www.linkedin.com/in/hassan-el-dada-b88190266/)