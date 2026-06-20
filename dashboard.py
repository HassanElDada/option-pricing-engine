import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# import our own modules
from src.black_scholes import black_scholes
from src.greeks import delta, gamma, vega, theta, rho
from src.monte_carlo import monte_carlo_price
from src.implied_volatility import implied_volatility

# --- page configuration ---
# this must be the first streamlit command in the file
# it sets the browser tab title and layout
st.set_page_config(
    page_title="Options Pricing Engine",
    page_icon="📈",
    layout="wide"
)

# --- title ---
#st.title is the large heading, markdown is markdown text
st.title("📈 Options Pricing and Volatility Analytics Engine")
st.markdown("Built with Black-Scholes, Monte Carlo simulation, and implied volatility solving.")

# --- tabs ---
# st.tabs creates a tabbed interface — each tab is a separate section
tab1, tab2, tab3 = st.tabs([
    "Black-Scholes Pricer",
    "Monte Carlo Simulation",
    "Implied Volatility"
])

# =============================================
# TAB 1 — BLACK-SCHOLES PRICER
# =============================================
#with tab1 makes everything indented inside it belong to Tab 1
with tab1:
    #st.header is smaller heading than st.title
    st.header("Black-Scholes Option Pricer")

    # --- sidebar-style inputs using columns ---
    # st.columns splits the page into side-by-side sections
    col1, col2 = st.columns([1, 2])
    #col2 is twice as wide as col1

    with col1:
        #everything with col1 appears on the left hand side 
        st.subheader("Parameters")

        # st.slider creates an interactive slider
        # arguments: label, min, max, default, step
        S = st.slider("Stock Price (S)", 50.0, 200.0, 100.0, 1.0)
        K = st.slider("Strike Price (K)", 50.0, 200.0, 100.0, 1.0)
        T = st.slider("Time to Maturity (years)", 0.1, 3.0, 1.0, 0.1)
        r = st.slider("Risk-Free Rate (%)", 0.0, 10.0, 5.0, 0.1) / 100
        sigma = st.slider("Volatility (%)", 1.0, 100.0, 20.0, 1.0) / 100
        option_type = st.radio("Option Type", ["call", "put"])
        #we divide r and sigma by 100 because the slider shows percentage but for black scholes
        #we expect a decimal 
        #st.radio creates radio buttons for the option type since they are discrete options


    with col2:
        #col2 appears on the right
        # --- prices ---
        #call black scholes with the slider values
        call_price = black_scholes(S, K, T, r, sigma, "call")
        put_price  = black_scholes(S, K, T, r, sigma, "put")

        st.subheader("Option Prices")
        price_col1, price_col2 = st.columns(2)
        #st.columns creates equal width columns inside the right column

        # st.metric displays a number with a label — looks clean and professional
        with price_col1:
            st.metric("Call Price", f"${call_price:.4f}")
        with price_col2:
            st.metric("Put Price", f"${put_price:.4f}")


        # --- Greeks table ---
        st.subheader("Greeks")

        call_delta = delta(S, K, T, r, sigma, "call")
        put_delta  = delta(S, K, T, r, sigma, "put")
        g          = gamma(S, K, T, r, sigma)
        v          = vega(S, K, T, r, sigma)
        call_theta = theta(S, K, T, r, sigma, "call")
        put_theta  = theta(S, K, T, r, sigma, "put")
        call_rho   = rho(S, K, T, r, sigma, "call")
        put_rho    = rho(S, K, T, r, sigma, "put")

        # st.dataframe displays a table from a dictionary
        #we import pandas here rather than the top since it's only used in this table
        import pandas as pd
        greeks_data = {
            "Greek": ["Delta", "Gamma", "Vega", "Theta", "Rho"],
            "Call":  [round(call_delta, 4), round(g, 4), round(v, 4), round(call_theta, 4), round(call_rho, 4)],
            "Put":   [round(put_delta, 4),  round(g, 4), round(v, 4), round(put_theta, 4),  round(put_rho, 4)],
            "Units": ["per $1 move", "per $1 move", "per 1% vol", "per day", "per 1% rate"]
        }
        st.dataframe(greeks_data, hide_index=True, use_container_width=True)

        # --- price vs stock plot ---
        st.subheader("Option Price vs Stock Price")


        #for plotting the values update live whenever the user moves a slider
        S_range = np.linspace(K * 0.5, K * 2, 200)
        call_prices = np.array([black_scholes(s, K, T, r, sigma, "call") for s in S_range])
        put_prices  = np.array([black_scholes(s, K, T, r, sigma, "put")  for s in S_range])

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(S_range, call_prices, label="Call Price", color="steelblue", linewidth=2)
        ax.plot(S_range, put_prices,  label="Put Price",  color="tomato",    linewidth=2)
        ax.axvline(x=S, color="gray", linestyle="--", linewidth=1, label=f"Current S = {S}")
        ax.axvline(x=K, color="black", linestyle=":", linewidth=1, label=f"Strike K = {K}")
        ax.set_xlabel("Stock Price")
        ax.set_ylabel("Option Price")
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()

        # st.pyplot displays a matplotlib figure in the app
        st.pyplot(fig)
        plt.close()

# =============================================
# TAB 2 — MONTE CARLO SIMULATION
# =============================================
with tab2:
    st.header("Monte Carlo Option Pricing")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Parameters")
        
        #streamlit requires every widget to have a unique label across the entire app
        #so now we use a trailing space to differentiate between this and the one in tab1
        S_mc    = st.slider("Stock Price (S) ", 50.0, 200.0, 100.0, 1.0)
        K_mc    = st.slider("Strike Price (K) ", 50.0, 200.0, 100.0, 1.0)
        T_mc    = st.slider("Time to Maturity (years) ", 0.1, 3.0, 1.0, 0.1)
        r_mc    = st.slider("Risk-Free Rate (%) ", 0.0, 10.0, 5.0, 0.1) / 100
        sigma_mc = st.slider("Volatility (%) ", 1.0, 100.0, 20.0, 1.0) / 100
        n_sims  = st.select_slider(
            "Number of Simulations",
            options=[1000, 5000, 10000, 50000, 100000],
            value=10000
        )
        ot_mc = st.radio("Option Type ", ["call", "put"])

    with col2:
        # run Monte Carlo
        mc_result = monte_carlo_price(S_mc, K_mc, T_mc, r_mc, sigma_mc, ot_mc,
                                       n_simulations=n_sims, seed=42)#seed 42 maintains reproducible results
        bs_price_mc = black_scholes(S_mc, K_mc, T_mc, r_mc, sigma_mc, ot_mc)

        st.subheader("Results")
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Black-Scholes", f"${bs_price_mc:.4f}")
        with m2:
            st.metric("Monte Carlo", f"${mc_result['price']:.4f}")
        with m3:
            st.metric("Antithetic", f"${mc_result['price_antithetic']:.4f}")

        st.caption(f"Std Error: {mc_result['std_error']:.4f} | Simulations: {n_sims:,}")
        #st.caption renders small grey text
        #n_sims:, adds comma seperators, so 100000 becomes 100,000

        # --- convergence plot ---
        st.subheader("Convergence Plot")

        sim_counts = np.logspace(2, 5, 40).astype(int)
        mc_prices_conv    = []
        anti_prices_conv  = []
        std_errors_conv   = []

        for n in sim_counts:
            res = monte_carlo_price(S_mc, K_mc, T_mc, r_mc, sigma_mc, ot_mc,
                                    n_simulations=n, seed=42)
            mc_prices_conv.append(res["price"])
            anti_prices_conv.append(res["price_antithetic"])
            std_errors_conv.append(res["std_error"])

        mc_prices_conv   = np.array(mc_prices_conv)
        anti_prices_conv = np.array(anti_prices_conv)
        std_errors_conv  = np.array(std_errors_conv)

        fig2, ax2 = plt.subplots(figsize=(8, 4))
        ax2.plot(sim_counts, mc_prices_conv,   label="Monte Carlo",        color="steelblue",   linewidth=2)
        ax2.plot(sim_counts, anti_prices_conv,  label="Antithetic Variates", color="mediumpurple", linewidth=2)
        ax2.axhline(y=bs_price_mc, color="tomato", linestyle="--", linewidth=1.5,
                    label=f"Black-Scholes = {bs_price_mc:.4f}")
        ax2.fill_between(sim_counts,
                         mc_prices_conv - 2 * std_errors_conv,
                         mc_prices_conv + 2 * std_errors_conv,
                         alpha=0.2, color="steelblue", label="95% Confidence Band")
        ax2.set_xscale("log")
        ax2.set_xlabel("Number of Simulations (log scale)")
        ax2.set_ylabel("Option Price")
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig2)
        plt.close()

# =============================================
# TAB 3 — IMPLIED VOLATILITY
# =============================================
with tab3:
    st.header("Implied Volatility Solver")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Parameters")
        S_iv    = st.slider("Stock Price (S)  ", 50.0, 200.0, 100.0, 1.0)
        K_iv    = st.slider("Strike Price (K)  ", 50.0, 200.0, 100.0, 1.0)
        T_iv    = st.slider("Time to Maturity (years)  ", 0.1, 3.0, 1.0, 0.1)
        r_iv    = st.slider("Risk-Free Rate (%)  ", 0.0, 10.0, 5.0, 0.1) / 100
        ot_iv   = st.radio("Option Type  ", ["call", "put"])
        mkt_price = st.number_input("Market Price", min_value=0.01, value=10.45, step=0.01)
        #st.numer_input creates text box with no up/down arrows, we use this instead of slider
        #since market prices can be any value

    with col2:
        # --- implied volatility solver ---
        st.subheader("Implied Volatility")
        #use try since user might enter price that violates no-arbitrage bounds
        #instead of app crashing, st.error displays UI error message 
        try:
            iv = implied_volatility(mkt_price, S_iv, K_iv, T_iv, r_iv, ot_iv)
            st.metric("Implied Volatility", f"{iv*100:.2f}%")

            bs_check = black_scholes(S_iv, K_iv, T_iv, r_iv, iv, ot_iv)
            st.caption(f"Verification — Black-Scholes price at recovered vol: ${bs_check:.4f} "
                       f"(market price: ${mkt_price:.4f})")

        except ValueError as e:
            st.error(f"Could not solve: {e}")

        # --- volatility smile ---
        st.subheader("Volatility Smile")

        K_range = np.linspace(S_iv * 0.7, S_iv * 1.3, 50)
        skew  = -0.05
        smile =  0.3
        implied_vols_smile = []

        for K_s in K_range:
            moneyness  = (K_s - S_iv) / S_iv
            true_sigma = max(0.2 + skew * moneyness + smile * moneyness**2, 0.01)
            price_s    = black_scholes(S_iv, K_s, T_iv, r_iv, true_sigma, "call")
            try:
                iv_s = implied_volatility(price_s, S_iv, K_s, T_iv, r_iv, "call")
                implied_vols_smile.append(iv_s * 100)
            except ValueError:
                implied_vols_smile.append(np.nan)

        fig3, ax3 = plt.subplots(figsize=(8, 4))
        ax3.plot(K_range, implied_vols_smile, color="steelblue", linewidth=2,
                 label="Implied Volatility")
        ax3.axvline(x=S_iv, color="tomato", linestyle="--", linewidth=1.5,
                    label=f"ATM = {S_iv}")
        ax3.set_xlabel("Strike Price (K)")
        ax3.set_ylabel("Implied Volatility (%)")
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig3)
        plt.close()