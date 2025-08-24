import streamlit as st
import numpy as np
import math
from scipy.stats import norm

# Page configuration
st.set_page_config(
    page_title="Options Pricer - Black-Scholes Model",
    page_icon="📈",
    layout="wide"
)

# Black-Scholes function (included directly to avoid import issues)
def blackScholes(S, K, T, r, sigma):
    """Calculate Black-Scholes option prices and Greeks"""
    if T <= 0 or sigma <= 0:
        return {
            'call_price': 0, 'put_price': 0,
            'delta_call': 0, 'delta_put': 0,
            'gamma': 0, 'theta_call': 0, 'theta_put': 0, 'vega': 0
        }
    
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    
    # Option prices
    call_price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    put_price = K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    
    # Greeks
    delta_call = norm.cdf(d1)
    delta_put = delta_call - 1
    gamma = norm.pdf(d1) / (S * sigma * math.sqrt(T))
    theta_call = (-S * norm.pdf(d1) * sigma / (2 * math.sqrt(T)) - 
                  r * K * math.exp(-r * T) * norm.cdf(d2))
    theta_put = (-S * norm.pdf(d1) * sigma / (2 * math.sqrt(T)) + 
                 r * K * math.exp(-r * T) * norm.cdf(-d2))
    vega = S * math.sqrt(T) * norm.pdf(d1)
    
    return {
        'call_price': call_price, 'put_price': put_price,
        'delta_call': delta_call, 'delta_put': delta_put,
        'gamma': gamma, 'theta_call': theta_call, 'theta_put': theta_put, 'vega': vega
    }

def main():
    st.title("📈 Options Pricer - Black-Scholes Model")
    
    # Sidebar for parameters
    with st.sidebar:
        st.header("🎛️ Parameters")
        
        S = st.slider("Stock Price (S)", 10.0, 200.0, 100.0, 1.0)
        K = st.slider("Strike Price (K)", 10.0, 200.0, 100.0, 1.0)
        T = st.slider("Time to Expiry (T)", 0.1, 5.0, 1.0, 0.1)
        r = st.slider("Risk-free Rate (r)", 0.0, 0.15, 0.05, 0.01)
        sigma = st.slider("Volatility (σ)", 0.05, 0.8, 0.2, 0.01)
    
    # Main content
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("💰 Option Prices")
        try:
            result = blackScholes(S, K, T, r, sigma)
            st.metric("Call Price", f"${result['call_price']:.4f}")
            st.metric("Put Price", f"${result['put_price']:.4f}")
            
            # Risk metrics
            moneyness = S / K
            intrinsic_call = max(0, S - K)
            time_value_call = result['call_price'] - intrinsic_call
            
            st.metric("Moneyness", f"{moneyness:.2f}")
            st.metric("Intrinsic Value (Call)", f"${intrinsic_call:.2f}")
            st.metric("Time Value (Call)", f"${time_value_call:.2f}")
        except Exception as e:
            st.error(f"Calculation error: {str(e)}")
    
    with col2:
        st.header("📊 Option Greeks")
        try:
            st.metric("Delta (Call)", f"{result['delta_call']:.4f}")
            st.metric("Delta (Put)", f"{result['delta_put']:.4f}")
            st.metric("Gamma", f"{result['gamma']:.4f}")
            st.metric("Theta (Call)", f"{result['theta_call']:.4f}")
            st.metric("Theta (Put)", f"{result['theta_put']:.4f}")
            st.metric("Vega", f"{result['vega']:.4f}")
        except Exception as e:
            st.error(f"Greeks calculation error: {str(e)}")
    
    # Simple chart using Streamlit's built-in charting
    st.header("📈 Sensitivity Analysis")
    
    # Create data for chart
    stock_prices = np.linspace(50, 150, 50)
    call_prices = []
    put_prices = []
    
    for s in stock_prices:
        try:
            res = blackScholes(s, K, T, r, sigma)
            call_prices.append(res['call_price'])
            put_prices.append(res['put_price'])
        except:
            call_prices.append(0)
            put_prices.append(0)
    
    # Create chart data
    chart_data = {
        'Stock Price': stock_prices,
        'Call Price': call_prices,
        'Put Price': put_prices
    }
    
    st.line_chart(chart_data)
    
    # Footer
    st.markdown("---")
    st.markdown("Built with Streamlit • Black-Scholes Model • Real-time Calculations")

if __name__ == "__main__":
    main() 